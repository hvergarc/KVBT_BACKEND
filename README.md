# KVBT - Autenticación Biométrica por Voz

KVBT es una API RESTful que permite enrolar, autenticar y verificar usuarios usando su voz como medio de identificación único. Diseñado para reemplazar o complementar métodos tradicionales como contraseñas o tokens.

---

## 🚀 Endpoints disponibles (v1.0.0)

### 1. `POST /api/enroll` - Enrolamiento de voz
Guarda la huella vocal de un usuario en la base local para futuros procesos de autenticación.

#### Parámetros (form-data):
| Clave     | Tipo    | Requerido | Descripción                             |
|----------|---------|-----------|-----------------------------------------|
| `userId` | string  | ✅         | Identificador único del usuario         |
| `audio`  | archivo | ✅         | Archivo `.wav` con la voz del usuario   |

#### Ejemplo en Postman:
- Método: `POST`  
- URL: `http://localhost:3000/api/enroll`
- Body: `form-data`  
  - `userId`: `usuario123`  
  - `audio`: `grabacion.wav`

#### Respuesta esperada:
```json
{
  "message": "Usuario enrolado exitosamente",
  "userId": "usuario123"
}
```

---

### 2. `POST /api/login` - Autenticación biométrica
Compara la voz enviada con la registrada previamente.

#### Parámetros (form-data):
| Clave     | Tipo    | Requerido | Descripción                             |
|----------|---------|-----------|-----------------------------------------|
| `userId` | string  | ✅         | Identificador del usuario               |
| `audio`  | archivo | ✅         | Audio `.wav` a validar                  |

#### Ejemplo en Postman:
- Método: `POST`  
- URL: `http://localhost:3000/api/login`
- Body: `form-data`  
  - `userId`: `usuario123`  
  - `audio`: `grabacion.wav`

#### Respuesta esperada:
```json
{
  "similarity": 0.89,
  "success": true,
  "userId": "usuario123"
}
```

---

### 3. `POST /api/verify` - Verificación vocal sin usuario (comparación directa)
Compara dos archivos de audio entre sí, sin necesidad de haber registrado previamente un usuario. Útil para pruebas rápidas o comparación entre voces arbitrarias.

#### Parámetros (form-data):
| Clave     | Tipo    | Requerido | Descripción                             |
|----------|---------|-----------|-----------------------------------------|
| `audio1` | archivo | ✅         | Primer archivo de voz (`.wav`)          |
| `audio2` | archivo | ✅         | Segundo archivo de voz (`.wav`)         |

#### Ejemplo en Postman:
- Método: `POST`  
- URL: `http://localhost:3000/api/verify`  
- Body: `form-data`  
  - `audio1`: `referencia.wav`  
  - `audio2`: `voz_a_validar.wav`

#### Respuesta esperada:
```json
{
  "similarity": 0.89,
  "success": true
}
```

---

## 🛠️ Tecnologías y librerías utilizadas
- **Python 3.10**
- **Flask** como framework web
- **SpeechBrain** para procesamiento de voz y generación de embeddings
- **scikit-learn** para similitud de vectores (cosine similarity)
- **NumPy** para manipulación numérica

---

## 🤖 Rol de la IA
Este proyecto fue construido junto a una inteligencia artificial generativa (ChatGPT), que participó activamente en cada paso del proceso.

---

## 🔐 KVBT = "Key Voice Biometric Token"
Una alternativa moderna y segura a JWT basada en biometría vocal. Ideal para sistemas donde se requiere autenticación sin contraseñas, con identidad vinculada directamente a la voz.

---

## 📌 Próximamente...
KVBT se convertirá en una **librería open-source**, para que cualquier sistema en cualquier lenguaje pueda integrarlo fácilmente con una simple llamada HTTP.

> "KVBT. La llave es tu voz."
