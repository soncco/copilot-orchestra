# ⚡ TravesIA - Quick Start

> Guía de inicio rápido en 5 minutos

---

## 🚀 Inicio en 3 Pasos

### 1️⃣ Backend (Django + Docker)

```bash
cd backend
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
# Email: admin@travesia.com, Password: admin123
```

✅ Backend corriendo en: http://localhost:8000

### 2️⃣ Frontend (Quasar 2)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend corriendo en: http://localhost:9000

### 3️⃣ Probar

1. Abre http://localhost:9000
2. Login con las credenciales del superuser
3. ¡Listo! Dashboard funcionando

---

## 📋 URLs Importantes

| Servicio     | URL                            | Descripción       |
| ------------ | ------------------------------ | ----------------- |
| **Frontend** | http://localhost:9000          | Aplicación Quasar |
| **API**      | http://localhost:8000/api/v1   | REST API          |
| **Admin**    | http://localhost:8000/admin    | Panel Django      |
| **Swagger**  | http://localhost:8000/api/docs | API Docs          |

---

## 🎯 ¿Qué sigue?

### Si eres Frontend Developer

**Próximo paso**: Implementar Programs CRUD page

```bash
cd frontend/src/pages/programs
# Crear: ProgramsListPage.vue, ProgramFormPage.vue
# Crear: ../services/programs.service.ts
```

**Tiempo estimado**: 3-4 horas
**Documentación**: [FRONTEND_COMPLETE.md](./FRONTEND_COMPLETE.md)

### Si eres Backend Developer

**Backend está 100% completo** ✅

**Puedes**:

- Agregar tests: `python manage.py test`
- Optimizar queries
- Agregar más endpoints si necesario

**Documentación**: [backend/STATUS.md](./backend/STATUS.md)

### Si eres Project Manager

**Ver estado visual**:

```bash
./PROJECT_STATUS.sh
```

**Progreso actual**:

- Backend: ✅ 100%
- Frontend: 🚧 30%
- Testing: ⏳ 0%

---

## 📚 Documentación Completa

| Documento                                      | Para qué sirve                     |
| ---------------------------------------------- | ---------------------------------- |
| [PROJECT-OVERVIEW.md](./PROJECT-OVERVIEW.md)   | Overview completo del proyecto ⭐  |
| [FRONTEND_COMPLETE.md](./FRONTEND_COMPLETE.md) | Frontend implementado detallado ⭐ |
| [backend/STATUS.md](./backend/STATUS.md)       | Backend APIs y modelos ⭐          |
| [docs/INDEX.md](./docs/INDEX.md)               | Índice de toda la documentación    |
| [SESSION_SUMMARY.md](./SESSION_SUMMARY.md)     | Resumen de la sesión de desarrollo |

---

## 🛠️ Comandos Útiles

```bash
# Ver estado del proyecto
./PROJECT_STATUS.sh

# Backend
cd backend
docker-compose up -d                          # Iniciar
docker-compose logs -f web                    # Ver logs
docker-compose exec web python manage.py shell  # Shell

# Frontend
cd frontend
npm run dev                                   # Dev server
npm run build                                 # Build
npm run lint                                  # Linter

# Ver documentación
cat docs/README.md
cat PROJECT-OVERVIEW.md
```

---

## ✅ Checklist Rápido

### Primera vez

- [ ] Docker instalado
- [ ] Node.js 18+ instalado
- [ ] PostgreSQL (vía Docker)
- [ ] `cd backend && docker-compose up -d`
- [ ] `cd frontend && npm install`

### Cada sesión de desarrollo

- [ ] `docker-compose up -d` (backend)
- [ ] `npm run dev` (frontend)
- [ ] Login en http://localhost:9000
- [ ] Verificar Swagger: http://localhost:8000/api/docs

---

## 🐛 Problemas Comunes

### "Backend no responde"

```bash
docker-compose ps        # Ver servicios
docker-compose restart web
```

### "Frontend no conecta"

1. Verificar backend: `curl http://localhost:8000/api/v1/`
2. Verificar `.env`: `VITE_API_BASE_URL=http://localhost:8000/api/v1`

### "MFA no funciona"

1. Sincronizar reloj (NTP)
2. Regenerar QR code

---

## 📞 Ayuda

- **Docs completas**: [docs/README.md](./docs/README.md)
- **Issues**: GitHub Issues
- **Email**: support@travesia.com

---

**Creado**: 22 Enero 2026
**Versión**: 1.0.0

**💡 Tip**: Siempre ejecuta `./PROJECT_STATUS.sh` primero!
