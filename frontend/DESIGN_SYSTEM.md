# TravesIA - Sistema de Diseño

## 🎨 Paleta de Colores

### Colores Principales

```scss
$primary: #0891b2; // Turquoise Blue
```

- **Uso**: Botones primarios, enlaces, elementos interactivos principales
- **Significado**: Confianza, profesionalismo, cielo, océano, viajes

```scss
$secondary: #f97316; // Warm Orange
```

- **Uso**: Botones secundarios, CTAs importantes, destacados
- **Significado**: Aventura, energía, atardeceres, calidez

```scss
$accent: #10b981; // Emerald Green
```

- **Uso**: Elementos de acento, badges, indicadores positivos
- **Significado**: Naturaleza, sostenibilidad, ecoturismo, frescura

### Colores de Estado

```scss
$positive: #22c55e   // Green
$negative: #ef4444   // Red
$info: #3b82f6       // Blue
$warning: #f59e0b    // Amber
```

### Colores Oscuros

```scss
$dark: #1e293b       // Slate Dark
$dark-page: #0f172a  // Slate Darker
```

## 🔤 Tipografía

### Fuente Principal: **Poppins**

- **Weights disponibles**: 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
- **Características**: Moderna, legible, profesional, amigable
- **Uso**: Toda la interfaz

### Jerarquía Tipográfica

```scss
// Títulos principales
h1 {
  font-size: 2.5rem;
  font-weight: 700;
}
h2 {
  font-size: 2rem;
  font-weight: 600;
}
h3 {
  font-size: 1.75rem;
  font-weight: 600;
}
h4 {
  font-size: 1.5rem;
  font-weight: 600;
}
h5 {
  font-size: 1.25rem;
  font-weight: 500;
}
h6 {
  font-size: 1rem;
  font-weight: 500;
}

// Texto
body {
  font-size: 1rem;
  font-weight: 400;
}
small {
  font-size: 0.875rem;
}
```

## 🌊 Gradientes

### Login Background

```scss
background: linear-gradient(135deg, #0891b2 0%, #0e7490 50%, #10b981 100%);
```

- Transición suave de turquesa a verde esmeralda
- Evoca cielo y naturaleza

### Botones Destacados (Opcional)

```scss
background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
```

- Para CTAs importantes

## 📐 Espaciado

Basado en múltiplos de 4px (sistema de 8pt grid):

- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px

## 🎯 Uso Recomendado

### Páginas de Marketing/Landing

- **Fondo**: Gradiente turquesa-verde
- **Título**: Blanco, Poppins Bold
- **Texto**: Blanco/Gris claro, Poppins Regular
- **CTA**: Naranja con hover más oscuro

### Dashboard/Aplicación

- **Fondo**: Blanco o gris muy claro
- **Navegación**: Slate dark
- **Botones primarios**: Turquesa
- **Elementos de acción**: Naranja
- **Indicadores positivos**: Verde esmeralda

### Formularios

- **Inputs**: Borde gris claro, focus azul turquesa
- **Labels**: Gris oscuro, Poppins Medium
- **Botón submit**: Turquesa primary
- **Errores**: Rojo negative

## ♿ Accesibilidad

- Todos los colores cumplen con WCAG AA para contraste
- Ratio mínimo 4.5:1 para texto normal
- Ratio mínimo 3:1 para texto grande (>18px)

## 📱 Responsive

La paleta funciona en todos los tamaños de pantalla sin necesidad de ajustes.

---

**Versión**: 1.0.0
**Fecha**: Enero 2026
