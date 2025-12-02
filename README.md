# MiniOffice — Firmado digital con certificado de prueba (self‑signed)

## 2️⃣ Crear un certificado de prueba (self-signed)
(Fuente: diapositiva 13)

Abrir PowerShell como Administrador y ejecutar:

```powershell
New-SelfSignedCertificate -Type CodeSigningCert -Subject "MiniOffice Test Code Signing" -CertStoreLocation Cert:\CurrentUser\My
```

Esto crea un certificado de firma de código dentro del almacén del usuario:

```
Cert:\CurrentUser\My
```

---

## 3️⃣ Comprobar el certificado creado
(Fuente: diapositiva 14)

1. Pulsa `Win + R`
2. Escribe: `certmgr.msc`
3. En la ventana, navega a: `Certificados → Personal → Certificados`
4. Debe aparecer: `MiniOffice Test Code Signing`

---

## 4️⃣ Exportar el certificado a un archivo .pfx
(Fuente: diapositiva 15)

En PowerShell:

4.1 Pedir contraseña (no se muestra en texto):
```powershell
$password = Read-Host "Introduce una contraseña para el archivo .pfx" -AsSecureString
```

4.2 Exportar el certificado:
```powershell
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object {$_.Subject -like "*MiniOffice Test Code Signing*"}
$pfxPath = "$env:USERPROFILE\Desktop\MiniOfficeTestCert.pfx"

Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password
```

Esto genera un archivo en tu escritorio: `MiniOfficeTestCert.pfx`.

---

## 5️⃣ Instalar el Windows SDK (para usar signtool)
(Fuente: diapositiva 16)

Instala: `Windows SDK Signing Tools for Desktop Apps`.

Esto añade el programa necesario: `signtool.exe`.

---

## 6️⃣ Localizar signtool.exe
(Fuente: diapositiva 17)

Rutas típicas:
```
C:\Program Files (x86)\Windows Kits\10\bin\VERSION\x64\signtool.exe
```
Ejemplo (según tu instalación):
```
C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe
```

---

## 7️⃣ Firmar MiniOffice.exe
(Fuente: diapositiva 18)

```powershell
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe" sign `
    /f "$env:USERPROFILE\Desktop\MiniOfficeTestCert.pfx" `
    /p TU_CONTRASEÑA `
    /fd SHA256 `
    /tr http://timestamp.digicert.com `
    /td sha256 `
    "RUTA\A\TU\EXE\MiniOffice.exe"
```

---

## 8️⃣ Verificar la firma digital

Opción A (PowerShell):
```powershell
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe" verify /pa "RUTA\A\TU\EXE\MiniOffice.exe"
```

Opción B (Windows):
- Clic derecho → Propiedades → pestaña "Firmas digitales"
- Debe aparecer tu certificado

---

## ✔ Conclusión
Tras estos pasos:
- Tienes un certificado self-signed
- Lo has exportado como .pfx
- Has firmado MiniOffice.exe
- Puedes verificar su firma desde Windows

---

## ¿Cómo subir este README a tu GitHub?

1. Guarda este archivo como `README.md`
2. Abre terminal en tu repositorio
3. Ejecuta:
```bash
git add README.md
git commit -m "Añadida documentación de firmado digital"
git push origin main
```
