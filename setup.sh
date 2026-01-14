#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Multi-Agent Orchestration System${NC}"
echo -e "${BLUE}  Bootstrap Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"

    cat > .env << 'EOF'
# Application
NODE_ENV=development
APP_URL=http://localhost:3000
PORT=3000

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# JWT
JWT_SECRET=your-secret-key-change-this
JWT_EXPIRES_IN=7d

# AWS S3 (optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=

# Stripe (optional)
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PUBLISHABLE_KEY=

# Email Service (Resend/SendGrid)
RESEND_API_KEY=
SENDGRID_API_KEY=

# OAuth (Google)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Monitoring (optional)
SENTRY_DSN=

# Feature Flags (optional)
FEATURE_FLAG_SERVICE=none
EOF

    echo -e "${GREEN}✅ .env file created. Please update with your credentials.${NC}\n"
else
    echo -e "${GREEN}✅ .env file already exists.${NC}\n"
fi

# Detect project type
if [ -f "package.json" ]; then
    PROJECT_TYPE="node"
    echo -e "${BLUE}📦 Detected Node.js project${NC}"
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="python"
    echo -e "${BLUE}🐍 Detected Python project${NC}"
else
    echo -e "${YELLOW}⚠️  No package.json or requirements.txt found.${NC}"
    echo -e "${YELLOW}This appears to be a template repository.${NC}"
    echo -e "${YELLOW}Initialize your project before running this script.${NC}\n"
    exit 0
fi

# Install dependencies
echo -e "\n${BLUE}📥 Installing dependencies...${NC}"

if [ "$PROJECT_TYPE" = "node" ]; then
    # Check for package manager
    if command -v pnpm &> /dev/null; then
        echo -e "${GREEN}Using pnpm${NC}"
        pnpm install
    elif command -v yarn &> /dev/null; then
        echo -e "${GREEN}Using yarn${NC}"
        yarn install
    else
        echo -e "${GREEN}Using npm${NC}"
        npm install
    fi

    echo -e "${GREEN}✅ Node dependencies installed${NC}"

elif [ "$PROJECT_TYPE" = "python" ]; then
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi

    echo -e "${GREEN}Activating virtual environment...${NC}"
    source venv/bin/activate

    echo -e "${GREEN}Installing Python packages...${NC}"

    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi

    if [ -f "pyproject.toml" ]; then
        pip install -e .
    fi

    echo -e "${GREEN}✅ Python dependencies installed${NC}"
fi

# Database setup
echo -e "\n${BLUE}🗄️  Setting up database...${NC}"

if [ "$PROJECT_TYPE" = "node" ]; then
    if [ -d "prisma" ]; then
        echo -e "${GREEN}Generating Prisma client...${NC}"
        npx prisma generate

        echo -e "${YELLOW}Do you want to run database migrations? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            npx prisma migrate dev
            echo -e "${GREEN}✅ Database migrated${NC}"
        else
            echo -e "${YELLOW}⏭️  Skipped migrations${NC}"
        fi
    else
        echo -e "${YELLOW}⏭️  No Prisma schema found${NC}"
    fi
fi

if [ "$PROJECT_TYPE" = "python" ]; then
    if [ -f "alembic.ini" ]; then
        echo -e "${GREEN}Running Alembic migrations...${NC}"

        echo -e "${YELLOW}Do you want to run database migrations? (y/n)${NC}"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            alembic upgrade head
            echo -e "${GREEN}✅ Database migrated${NC}"
        else
            echo -e "${YELLOW}⏭️  Skipped migrations${NC}"
        fi
    else
        echo -e "${YELLOW}⏭️  No Alembic configuration found${NC}"
    fi
fi

# Git hooks setup
echo -e "\n${BLUE}🔧 Setting up Git hooks...${NC}"

if [ -d ".git" ]; then
    if command -v husky &> /dev/null || [ -f "node_modules/.bin/husky" ]; then
        npx husky install
        echo -e "${GREEN}✅ Husky hooks installed${NC}"
    elif [ -d ".git/hooks" ]; then
        # Create pre-commit hook manually
        cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
echo "Running pre-commit checks..."

# Run linter
if [ -f "package.json" ]; then
    npm run lint --silent || exit 1
fi

# Run tests
if [ -f "package.json" ]; then
    npm run test --silent || exit 1
fi

echo "✅ Pre-commit checks passed"
HOOK
        chmod +x .git/hooks/pre-commit
        echo -e "${GREEN}✅ Git pre-commit hook created${NC}"
    fi
else
    echo -e "${YELLOW}⏭️  Not a git repository${NC}"
fi

# Create necessary directories
echo -e "\n${BLUE}📁 Creating project directories...${NC}"

mkdir -p logs
mkdir -p uploads
mkdir -p temp
mkdir -p backups

echo -e "${GREEN}✅ Directories created${NC}"

# Validate configuration
echo -e "\n${BLUE}🔍 Validating configuration...${NC}"

if [ -f "project-context.md" ]; then
    echo -e "${GREEN}✅ project-context.md found${NC}"
else
    echo -e "${RED}❌ project-context.md not found${NC}"
fi

if [ -f "agents-config.json" ]; then
    echo -e "${GREEN}✅ agents-config.json found${NC}"
else
    echo -e "${RED}❌ agents-config.json not found${NC}"
fi

if [ -d ".github/agents" ]; then
    agent_count=$(ls -1 .github/agents/*.md 2>/dev/null | wc -l)
    echo -e "${GREEN}✅ Found ${agent_count} agent definitions${NC}"
else
    echo -e "${RED}❌ .github/agents directory not found${NC}"
fi

# Security checks
echo -e "\n${BLUE}🔒 Security checks...${NC}"

if [ -f ".env" ]; then
    if grep -q "your-secret-key-change-this" .env; then
        echo -e "${RED}⚠️  WARNING: Default JWT_SECRET detected!${NC}"
        echo -e "${YELLOW}Please change JWT_SECRET in .env file${NC}"
    fi

    if grep -q "DATABASE_URL=\"postgresql://user:password@" .env; then
        echo -e "${RED}⚠️  WARNING: Default database credentials detected!${NC}"
        echo -e "${YELLOW}Please update DATABASE_URL in .env file${NC}"
    fi
fi

# Final instructions
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete! 🎉${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}Next steps:${NC}\n"

echo -e "1. ${YELLOW}Update .env file with your credentials${NC}"
echo -e "2. ${YELLOW}Review project-context.md and update variables${NC}"
echo -e "3. ${YELLOW}Run database migrations if you haven't yet${NC}"

if [ "$PROJECT_TYPE" = "node" ]; then
    echo -e "4. ${YELLOW}Start development server:${NC}"
    echo -e "   ${GREEN}npm run dev${NC}"
    echo -e "\n5. ${YELLOW}Run tests:${NC}"
    echo -e "   ${GREEN}npm test${NC}"
fi

if [ "$PROJECT_TYPE" = "python" ]; then
    echo -e "4. ${YELLOW}Activate virtual environment:${NC}"
    echo -e "   ${GREEN}source venv/bin/activate${NC}"
    echo -e "\n5. ${YELLOW}Start development server:${NC}"
    echo -e "   ${GREEN}python manage.py runserver${NC} (Django)"
    echo -e "   ${GREEN}uvicorn main:app --reload${NC} (FastAPI)"
fi

echo -e "\n${BLUE}Documentation:${NC}"
echo -e "  - Agent system: ${GREEN}CONTRIBUTING.md${NC}"
echo -e "  - API docs: ${GREEN}docs/api/README.md${NC}"
echo -e "  - Architecture: ${GREEN}docs/architecture/ADR.md${NC}"

echo -e "\n${BLUE}Useful commands:${NC}"
echo -e "  ${GREEN}npm run lint${NC}          # Run linter"
echo -e "  ${GREEN}npm run format${NC}        # Format code"
echo -e "  ${GREEN}npm run test:watch${NC}    # Run tests in watch mode"
echo -e "  ${GREEN}npm run build${NC}         # Build for production"

echo -e "\n${YELLOW}Don't forget to read CONTRIBUTING.md to understand the agent workflow!${NC}\n"
