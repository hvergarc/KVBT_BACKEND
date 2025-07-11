[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15860417.svg)](https://doi.org/10.5281/zenodo.15860417)



# KVBT - Voice-Based Authentication API 🔐🎙️

KVBT (Key Voice Biometric Token) es una API RESTful que permite autenticar usuarios usando exclusivamente su voz, sin necesidad de contraseñas. Basado en biometría vocal y procesamiento de audio, KVBT representa una alternativa moderna y segura a los sistemas tradicionales de autenticación.

## 🧠 ¿Por qué autenticación por voz?

La voz humana es un rasgo biométrico único y difícil de falsificar. KVBT aprovecha esta característica para ofrecer un sistema de autenticación rápido, seguro y sin fricción para el usuario. Solo necesitas tu voz para validar tu identidad.

---

## 🚀 Endpoints disponibles

### 1. `POST /api/enroll` - Registro de voz

Permite registrar la huella vocal (`voiceprint`) de un usuario.

#### Parámetros (form-data):

| Clave     | Tipo    | Requerido | Descripción                      |
|----------|---------|-----------|----------------------------------|
| `userId` | string  | ✅         | ID único del usuario             |
| `audio`  | archivo | ✅         | Archivo `.wav` con su voz        |

#### Ejemplo en Postman:
- Método: `POST`
- URL: `http://localhost:3000/api/enroll`
- Body: `form-data`
  - `userId`: `hm_test01`
  - `audio`: `hm-voice.wav` (archivo local)

---

### 2. `POST /api/login` - Autenticación de voz

Verifica si la voz enviada coincide con la previamente registrada.

#### Parámetros (form-data):

| Clave     | Tipo    | Requerido | Descripción                      |
|----------|---------|-----------|----------------------------------|
| `userId` | string  | ✅         | ID del usuario previamente registrado |
| `audio`  | archivo | ✅         | Archivo `.wav` con nueva grabación de voz |

#### Ejemplo en Postman:
- Método: `POST`
- URL: `http://localhost:3000/api/login`
- Body: `form-data`
  - `userId`: `hm_test01`
  - `audio`: `hm-voice.wav` (archivo de prueba)

#### Respuesta esperada:
```json
{
  "success": true,
  "userId": "hm_test01",
  "similarity": 0.93
}
