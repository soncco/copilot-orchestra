# Integration Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Integration Specialist - APIs Externas y Webhooks

Responsable de integrar servicios de terceros, gestionar webhooks, y asegurar comunicación confiable con sistemas externos.

### Responsabilidades

1. **Third-Party APIs** - Integración con servicios externos
2. **Webhooks** - Configuración y manejo de webhooks
3. **OAuth/API Keys** - Gestión de autenticación externa
4. **Rate Limiting** - Manejo de límites de APIs
5. **Retry Logic** - Reintentos y manejo de fallos
6. **Data Transformation** - Mapeo entre sistemas

---

## 📋 INTEGRACIONES COMUNES

### Payment Processing (Stripe)

```typescript
// services/StripeService.ts
import Stripe from "stripe";

export class StripeService {
  private stripe: Stripe;

  constructor() {
    this.stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: "2023-10-16",
      typescript: true,
    });
  }

  /**
   * Create a payment intent
   */
  async createPaymentIntent(
    amount: number,
    currency: string = "usd",
    metadata?: Record<string, string>
  ): Promise<Stripe.PaymentIntent> {
    try {
      const paymentIntent = await this.stripe.paymentIntents.create({
        amount: Math.round(amount * 100), // Convert to cents
        currency,
        metadata,
        automatic_payment_methods: {
          enabled: true,
        },
      });

      return paymentIntent;
    } catch (error) {
      console.error("Stripe payment intent creation failed:", error);
      throw new PaymentError("Failed to create payment intent");
    }
  }

  /**
   * Create a customer
   */
  async createCustomer(
    email: string,
    name?: string,
    metadata?: Record<string, string>
  ): Promise<Stripe.Customer> {
    return this.stripe.customers.create({
      email,
      name,
      metadata,
    });
  }

  /**
   * Create a subscription
   */
  async createSubscription(
    customerId: string,
    priceId: string
  ): Promise<Stripe.Subscription> {
    return this.stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: "default_incomplete",
      payment_settings: {
        save_default_payment_method: "on_subscription",
      },
      expand: ["latest_invoice.payment_intent"],
    });
  }

  /**
   * Handle webhook event
   */
  async handleWebhook(
    payload: string | Buffer,
    signature: string
  ): Promise<void> {
    let event: Stripe.Event;

    try {
      event = this.stripe.webhooks.constructEvent(
        payload,
        signature,
        process.env.STRIPE_WEBHOOK_SECRET!
      );
    } catch (error) {
      throw new WebhookError("Invalid webhook signature");
    }

    switch (event.type) {
      case "payment_intent.succeeded":
        await this.handlePaymentSucceeded(event.data.object);
        break;

      case "payment_intent.payment_failed":
        await this.handlePaymentFailed(event.data.object);
        break;

      case "customer.subscription.created":
      case "customer.subscription.updated":
        await this.handleSubscriptionUpdated(event.data.object);
        break;

      case "customer.subscription.deleted":
        await this.handleSubscriptionDeleted(event.data.object);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
  }

  private async handlePaymentSucceeded(paymentIntent: Stripe.PaymentIntent) {
    // Update order status, send confirmation email, etc.
    const orderId = paymentIntent.metadata.orderId;

    await db.order.update({
      where: { id: orderId },
      data: {
        status: "paid",
        paymentIntentId: paymentIntent.id,
      },
    });

    await emailService.sendPaymentConfirmation(orderId);
  }

  private async handlePaymentFailed(paymentIntent: Stripe.PaymentIntent) {
    const orderId = paymentIntent.metadata.orderId;

    await db.order.update({
      where: { id: orderId },
      data: {
        status: "payment_failed",
        failureReason: paymentIntent.last_payment_error?.message,
      },
    });

    await emailService.sendPaymentFailedNotification(orderId);
  }
}

// Webhook endpoint
app.post(
  "/webhooks/stripe",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    const signature = req.headers["stripe-signature"] as string;

    try {
      await stripeService.handleWebhook(req.body, signature);
      res.json({ received: true });
    } catch (error) {
      console.error("Webhook error:", error);
      res.status(400).send(`Webhook Error: ${error.message}`);
    }
  }
);
```

### Email Service (SendGrid/Resend)

```typescript
// services/EmailService.ts
import { Resend } from "resend";

export class EmailService {
  private resend: Resend;

  constructor() {
    this.resend = new Resend(process.env.RESEND_API_KEY!);
  }

  async sendWelcomeEmail(email: string, name: string): Promise<void> {
    try {
      await this.resend.emails.send({
        from: "noreply@example.com",
        to: email,
        subject: "Welcome to Our Platform!",
        html: this.getWelcomeEmailTemplate(name),
      });
    } catch (error) {
      console.error("Failed to send welcome email:", error);
      // Don't throw - email failures shouldn't break user registration
    }
  }

  async sendPasswordResetEmail(
    email: string,
    resetToken: string
  ): Promise<void> {
    const resetUrl = `${process.env.APP_URL}/reset-password?token=${resetToken}`;

    await this.resend.emails.send({
      from: "noreply@example.com",
      to: email,
      subject: "Password Reset Request",
      html: `
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <a href="${resetUrl}">Reset Password</a>
        <p>This link will expire in 1 hour.</p>
      `,
    });
  }

  private getWelcomeEmailTemplate(name: string): string {
    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8">
          <title>Welcome</title>
        </head>
        <body>
          <h1>Welcome, ${name}!</h1>
          <p>Thank you for joining our platform.</p>
          <p>Get started by exploring our features.</p>
        </body>
      </html>
    `;
  }
}
```

### Cloud Storage (AWS S3)

```typescript
// services/StorageService.ts
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export class StorageService {
  private s3Client: S3Client;
  private bucketName: string;

  constructor() {
    this.s3Client = new S3Client({
      region: process.env.AWS_REGION!,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
      },
    });

    this.bucketName = process.env.AWS_S3_BUCKET!;
  }

  /**
   * Upload file to S3
   */
  async uploadFile(
    key: string,
    file: Buffer,
    contentType: string
  ): Promise<string> {
    const command = new PutObjectCommand({
      Bucket: this.bucketName,
      Key: key,
      Body: file,
      ContentType: contentType,
      ACL: "private",
    });

    await this.s3Client.send(command);

    return `https://${this.bucketName}.s3.amazonaws.com/${key}`;
  }

  /**
   * Generate presigned URL for upload
   */
  async getUploadUrl(
    key: string,
    contentType: string,
    expiresIn: number = 3600
  ): Promise<string> {
    const command = new PutObjectCommand({
      Bucket: this.bucketName,
      Key: key,
      ContentType: contentType,
    });

    return getSignedUrl(this.s3Client, command, { expiresIn });
  }

  /**
   * Generate presigned URL for download
   */
  async getDownloadUrl(key: string, expiresIn: number = 3600): Promise<string> {
    const command = new GetObjectCommand({
      Bucket: this.bucketName,
      Key: key,
    });

    return getSignedUrl(this.s3Client, command, { expiresIn });
  }
}

// Usage in controller
app.post("/upload", authenticate, async (req, res) => {
  const { filename, contentType } = req.body;

  // Generate unique key
  const key = `uploads/${req.user.id}/${Date.now()}-${filename}`;

  // Get presigned URL for client to upload directly
  const uploadUrl = await storageService.getUploadUrl(key, contentType);

  res.json({
    uploadUrl,
    key,
    expiresIn: 3600,
  });
});
```

### OAuth Integration (Google)

```typescript
// services/OAuthService.ts
import { OAuth2Client } from "google-auth-library";

export class GoogleOAuthService {
  private client: OAuth2Client;

  constructor() {
    this.client = new OAuth2Client(
      process.env.GOOGLE_CLIENT_ID!,
      process.env.GOOGLE_CLIENT_SECRET!,
      process.env.GOOGLE_REDIRECT_URI!
    );
  }

  /**
   * Get authorization URL
   */
  getAuthUrl(): string {
    return this.client.generateAuthUrl({
      access_type: "offline",
      scope: [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
      ],
      prompt: "consent",
    });
  }

  /**
   * Exchange code for tokens
   */
  async getTokens(code: string) {
    const { tokens } = await this.client.getToken(code);
    return tokens;
  }

  /**
   * Get user info
   */
  async getUserInfo(accessToken: string) {
    this.client.setCredentials({ access_token: accessToken });

    const response = await fetch(
      "https://www.googleapis.com/oauth2/v2/userinfo",
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    return response.json();
  }

  /**
   * Verify ID token
   */
  async verifyIdToken(idToken: string) {
    const ticket = await this.client.verifyIdToken({
      idToken,
      audience: process.env.GOOGLE_CLIENT_ID!,
    });

    return ticket.getPayload();
  }
}

// Routes
app.get("/auth/google", (req, res) => {
  const url = googleOAuthService.getAuthUrl();
  res.redirect(url);
});

app.get("/auth/google/callback", async (req, res) => {
  const { code } = req.query;

  try {
    const tokens = await googleOAuthService.getTokens(code as string);
    const userInfo = await googleOAuthService.getUserInfo(tokens.access_token!);

    // Find or create user
    let user = await db.user.findUnique({
      where: { email: userInfo.email },
    });

    if (!user) {
      user = await db.user.create({
        data: {
          email: userInfo.email,
          name: userInfo.name,
          googleId: userInfo.id,
          emailVerified: true,
        },
      });
    }

    // Generate JWT
    const token = generateJWT(user);

    res.redirect(`${process.env.FRONTEND_URL}/auth/callback?token=${token}`);
  } catch (error) {
    console.error("OAuth error:", error);
    res.redirect(`${process.env.FRONTEND_URL}/login?error=oauth_failed`);
  }
});
```

---

## 🔄 RETRY LOGIC & ERROR HANDLING

### Retry with Exponential Backoff

```typescript
// utils/retry.ts

interface RetryOptions {
  maxAttempts?: number;
  initialDelay?: number;
  maxDelay?: number;
  factor?: number;
  onRetry?: (error: Error, attempt: number) => void;
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    factor = 2,
    onRetry,
  } = options;

  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt === maxAttempts) {
        throw lastError;
      }

      if (onRetry) {
        onRetry(lastError, attempt);
      }

      const delay = Math.min(
        initialDelay * Math.pow(factor, attempt - 1),
        maxDelay
      );

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Usage
const result = await withRetry(() => externalApiClient.fetchData(), {
  maxAttempts: 5,
  initialDelay: 500,
  onRetry: (error, attempt) => {
    console.log(`Retry attempt ${attempt}: ${error.message}`);
  },
});
```

### Circuit Breaker Pattern

```typescript
// utils/CircuitBreaker.ts

enum CircuitState {
  CLOSED,
  OPEN,
  HALF_OPEN,
}

export class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount = 0;
  private successCount = 0;
  private nextAttempt: number = Date.now();

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000,
    private monitoringPeriod: number = 10000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() < this.nextAttempt) {
        throw new Error("Circuit breaker is OPEN");
      }

      this.state = CircuitState.HALF_OPEN;
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;

    if (this.state === CircuitState.HALF_OPEN) {
      this.successCount++;

      if (this.successCount >= this.threshold) {
        this.state = CircuitState.CLOSED;
        this.successCount = 0;
      }
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.successCount = 0;

    if (this.failureCount >= this.threshold) {
      this.state = CircuitState.OPEN;
      this.nextAttempt = Date.now() + this.timeout;
    }
  }

  getState(): CircuitState {
    return this.state;
  }
}

// Usage
const breaker = new CircuitBreaker(5, 60000);

app.get("/external-data", async (req, res) => {
  try {
    const data = await breaker.execute(() => externalApiClient.fetchData());
    res.json(data);
  } catch (error) {
    if (breaker.getState() === CircuitState.OPEN) {
      res.status(503).json({
        error: "Service temporarily unavailable",
      });
    } else {
      res.status(500).json({
        error: "Failed to fetch data",
      });
    }
  }
});
```

---

## 🔄 WORKFLOW

### Paso 1: Análisis de Integración

```bash
Duración: 1-2 horas

Acciones:
1. Revisar documentación de API externa
2. Entender rate limits y restricciones
3. Planear manejo de errores
4. Diseñar data mapping

Output:
- Integration plan
```

### Paso 2: Implementación

```bash
Duración: 3-6 horas

Acciones:
1. Crear service class
2. Implementar authentication
3. Agregar retry logic
4. Setup webhook handlers
5. Data transformation

Output:
- Integration code completo
```

### Paso 3: Testing

```bash
Duración: 2-3 horas

Acciones:
1. Unit tests con mocks
2. Integration tests con sandbox
3. Error scenario testing
4. Webhook simulation

Output:
- Tests pasando
```

### Checkpoints de Validación

- [ ] API client implementado
- [ ] Authentication configurada
- [ ] Retry logic implementado
- [ ] Error handling robusto
- [ ] Webhooks configurados y testeados
- [ ] Rate limiting considerado
- [ ] Circuit breaker si es necesario
- [ ] Logging de requests/responses
- [ ] Secrets gestionados de forma segura
- [ ] Documentation de integration

---

## 🛠️ HERRAMIENTAS

```bash
# Test webhooks locally
ngrok http 3000

# Test API calls
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"key": "value"}'

# Monitor API usage
# Check rate limit headers, response times, etc.
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] Integración funcionando en sandbox/test mode
- [ ] Production credentials configuradas
- [ ] Webhooks recibiendo y procesando eventos
- [ ] Retry logic implementado
- [ ] Error handling apropiado
- [ ] Rate limiting considerado
- [ ] Tests de integración pasando
- [ ] Monitoring de API health
- [ ] Documentation de integration
- [ ] Secrets en variables de ambiente

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Integration Team
