#!/bin/bash

# Script para mostrar el estado actual del proyecto TravesIA
# Ejecutar: chmod +x ./PROJECT_STATUS.sh && ./PROJECT_STATUS.sh

clear

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner
echo -e "${BLUE}${BOLD}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ████████╗██████╗  █████╗ ██╗   ██╗███████╗███████╗██╗ █████╗    ║
║   ╚══██╔══╝██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██║██╔══██╗   ║
║      ██║   ██████╔╝███████║██║   ██║█████╗  ███████╗██║███████║   ║
║      ██║   ██╔══██╗██╔══██║╚██╗ ██╔╝██╔══╝  ╚════██║██║██╔══██║   ║
║      ██║   ██║  ██║██║  ██║ ╚████╔╝ ███████╗███████║██║██║  ██║   ║
║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝   ║
║                                                              ║
║          Sistema de Gestión Turística - Version 1.0          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BOLD}📊 ESTADO DEL PROYECTO${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Stack Tecnológico
echo -e "${YELLOW}${BOLD}🏗️  STACK TECNOLÓGICO${NC}"
echo ""
echo -e "  ${GREEN}Backend:${NC}  Django 5.0 + DRF 3.14 + PostgreSQL 15 + Redis 7"
echo -e "  ${GREEN}Frontend:${NC} Vue 3 + Quasar 2 + TypeScript + Pinia + Axios"
echo -e "  ${GREEN}DevOps:${NC}  Docker + Docker Compose + AWS S3"
echo ""

# Backend Status
echo -e "${YELLOW}${BOLD}⚙️  BACKEND (Django) - COMPLETADO ✅${NC}"
echo ""
echo -e "  ${GREEN}✅${NC} 6 apps Django implementadas"
echo -e "  ${GREEN}✅${NC} 22 modelos de base de datos"
echo -e "  ${GREEN}✅${NC} 50+ endpoints REST API"
echo -e "  ${GREEN}✅${NC} Autenticación JWT + MFA (TOTP)"
echo -e "  ${GREEN}✅${NC} 5 roles de usuario (Admin, Manager, Sales, Guide, Ops)"
echo -e "  ${GREEN}✅${NC} Swagger/OpenAPI documentation"
echo -e "  ${GREEN}✅${NC} Docker Compose environment"
echo -e "  ${GREEN}✅${NC} Celery para tareas asíncronas"
echo ""
echo -e "  ${BLUE}Apps implementadas:${NC}"
echo -e "    • authentication - Users, MFA, Audit Log"
echo -e "    • circuits - Programs, Groups, Passengers, Itineraries, Flights"
echo -e "    • suppliers - Suppliers, Services, Pricing, Exchange Rates"
echo -e "    • operations - Hotels, Transportation, Staff, Services"
echo -e "    • financial - Invoices, Costs, Sales, Commissions, Bank Deposits"
echo -e "    • documents - Document management con S3"
echo ""

# Frontend Status
echo -e "${YELLOW}${BOLD}🎨 FRONTEND (Quasar 2) - EN DESARROLLO 🚧${NC}"
echo ""
echo -e "  ${GREEN}✅${NC} Proyecto Quasar creado con TypeScript"
echo -e "  ${GREEN}✅${NC} Axios API client con interceptors"
echo -e "  ${GREEN}✅${NC} TypeScript types para todas las entidades"
echo -e "  ${GREEN}✅${NC} Servicio de autenticación completo"
echo -e "  ${GREEN}✅${NC} Pinia store (auth) configurado"
echo -e "  ${GREEN}✅${NC} Login page con soporte MFA"
echo -e "  ${GREEN}✅${NC} Dashboard con estadísticas"
echo -e "  ${GREEN}✅${NC} MainLayout con sidebar navigation"
echo -e "  ${GREEN}✅${NC} Route guards para protección"
echo -e "  ${GREEN}✅${NC} Environment configuration (.env)"
echo ""
echo -e "  ${BLUE}Páginas implementadas (2 de 13):${NC}"
echo -e "    ${GREEN}✅${NC} LoginPage - Autenticación con MFA"
echo -e "    ${GREEN}✅${NC} DashboardPage - Vista general"
echo ""
echo -e "  ${RED}⏳${NC} ${BLUE}Páginas pendientes (11):${NC}"
echo -e "    ⏳ Programs - Gestión de circuitos"
echo -e "    ⏳ Groups - Gestión de grupos"
echo -e "    ⏳ Passengers - Gestión de pasajeros"
echo -e "    ⏳ Suppliers - Gestión de proveedores"
echo -e "    ⏳ Hotels - Gestión de hoteles"
echo -e "    ⏳ Transportation - Gestión de transporte"
echo -e "    ⏳ Financial - Facturas y finanzas"
echo -e "    ⏳ Documents - Gestión de documentos"
echo -e "    ⏳ Calendar - Vista de calendario"
echo -e "    ⏳ Reports - Reportes y analytics"
echo -e "    ⏳ Profile & Settings - Perfil y configuración"
echo ""

# Progreso General
echo -e "${YELLOW}${BOLD}📈 PROGRESO GENERAL${NC}"
echo ""
echo -e "  Backend API:           ${GREEN}[████████████████████] 100%${NC}"
echo -e "  Frontend Foundation:   ${GREEN}[████████████████████] 100%${NC}"
echo -e "  Frontend CRUD Pages:   ${YELLOW}[███░░░░░░░░░░░░░░░░░]  15%${NC}"
echo -e "  Testing:               ${RED}[░░░░░░░░░░░░░░░░░░░░]   0%${NC}"
echo -e "  Documentation:         ${GREEN}[███████████████░░░░░]  75%${NC}"
echo ""
echo -e "  ${BOLD}Total del proyecto:    ${YELLOW}[██████░░░░░░░░░░░░░░]  30%${NC}"
echo ""

# Próximos Pasos
echo -e "${YELLOW}${BOLD}🎯 PRÓXIMOS PASOS${NC}"
echo ""
echo -e "  ${BLUE}1.${NC} Test de integración frontend-backend"
echo -e "  ${BLUE}2.${NC} Implementar Programs CRUD page"
echo -e "  ${BLUE}3.${NC} Implementar Groups CRUD page"
echo -e "  ${BLUE}4.${NC} Implementar Passengers CRUD page"
echo -e "  ${BLUE}5.${NC} Crear componentes reutilizables (DataTable, Forms)"
echo -e "  ${BLUE}6.${NC} Implementar páginas restantes"
echo -e "  ${BLUE}7.${NC} Sistema de reportes"
echo -e "  ${BLUE}8.${NC} Integración SUNAT"
echo ""

# URLs de Acceso
echo -e "${YELLOW}${BOLD}🌐 URLs DE ACCESO${NC}"
echo ""
echo -e "  ${GREEN}Frontend:${NC}      http://localhost:9000"
echo -e "  ${GREEN}Backend API:${NC}   http://localhost:8000/api/v1"
echo -e "  ${GREEN}Django Admin:${NC}  http://localhost:8000/admin"
echo -e "  ${GREEN}Swagger Docs:${NC}  http://localhost:8000/api/docs"
echo -e "  ${GREEN}ReDoc:${NC}         http://localhost:8000/api/redoc"
echo ""

# Comandos Útiles
echo -e "${YELLOW}${BOLD}🚀 COMANDOS ÚTILES${NC}"
echo ""
echo -e "  ${BLUE}# Backend (Docker)${NC}"
echo -e "  cd backend && docker-compose up -d"
echo -e "  docker-compose exec web python manage.py migrate"
echo -e "  docker-compose exec web python manage.py createsuperuser"
echo -e "  docker-compose logs -f web"
echo ""
echo -e "  ${BLUE}# Frontend${NC}"
echo -e "  cd frontend && npm install"
echo -e "  npm run dev"
echo -e "  npm run build"
echo ""
echo -e "  ${BLUE}# Testing${NC}"
echo -e "  cd backend && python manage.py test"
echo -e "  cd frontend && npm run test"
echo ""

# Estructura de Archivos
echo -e "${YELLOW}${BOLD}📁 ESTRUCTURA DEL PROYECTO${NC}"
echo ""
echo -e "  ericxpeditions/"
echo -e "  ├── ${GREEN}backend/${NC}          Django API (✅ Completo)"
echo -e "  │   ├── apps/         6 Django apps"
echo -e "  │   ├── config/       Settings y URLs"
echo -e "  │   └── core/         Utilities"
echo -e "  ├── ${YELLOW}frontend/${NC}         Quasar 2 (🚧 En desarrollo)"
echo -e "  │   ├── src/"
echo -e "  │   │   ├── pages/    2 de 13 páginas"
echo -e "  │   │   ├── layouts/  MainLayout"
echo -e "  │   │   ├── services/ API client"
echo -e "  │   │   ├── stores/   Pinia stores"
echo -e "  │   │   └── types/    TypeScript types"
echo -e "  ├── docs/            Documentación"
echo -e "  └── .github/         Agentes y configuración"
echo ""

# Footer
echo -e "${BLUE}${BOLD}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  💡 Tip: Ejecuta 'cd frontend && npm run dev' para iniciar"
echo "  📚 Ver PROJECT-OVERVIEW.md para información completa"
echo "  🐛 Reportar issues en GitHub"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo -e "${NC}"

# Verificar si Docker está corriendo
echo -e "${YELLOW}${BOLD}🔍 VERIFICACIÓN DE SERVICIOS${NC}"
echo ""

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "  ${GREEN}✅${NC} Docker instalado"

    # Check if backend is running
    if docker ps | grep -q "backend"; then
        echo -e "  ${GREEN}✅${NC} Backend Docker container corriendo"
    else
        echo -e "  ${RED}❌${NC} Backend Docker container no está corriendo"
        echo -e "     ${YELLOW}→${NC} Ejecutar: cd backend && docker-compose up -d"
    fi
else
    echo -e "  ${RED}❌${NC} Docker no está instalado"
fi

# Check Node
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo -e "  ${GREEN}✅${NC} Node.js $NODE_VERSION instalado"
else
    echo -e "  ${RED}❌${NC} Node.js no está instalado"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo -e "  ${GREEN}✅${NC} npm $NPM_VERSION instalado"
else
    echo -e "  ${RED}❌${NC} npm no está instalado"
fi

# Check if frontend dependencies are installed
if [ -d "frontend/node_modules" ]; then
    echo -e "  ${GREEN}✅${NC} Frontend dependencies instaladas"
else
    echo -e "  ${RED}❌${NC} Frontend dependencies no instaladas"
    echo -e "     ${YELLOW}→${NC} Ejecutar: cd frontend && npm install"
fi

echo ""
echo -e "${GREEN}${BOLD}✨ ¡Todo listo para desarrollar! ✨${NC}"
echo ""
