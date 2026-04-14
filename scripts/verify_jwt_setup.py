#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de JWT Implementation
Ejecutar antes de iniciar el sistema
"""

import os
import sys
import subprocess
from pathlib import Path

class JWTChecklist:
    def __init__(self):
        self.backend_path = Path("C:/Users/Richar/Desktop/Fast api 0.1.3")
        self.frontend_path = Path("C:/Users/Richar/Desktop/Fronted 1.2.2")
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check_file_exists(self, path, name):
        """Verifica que un archivo exista"""
        if Path(path).exists():
            print(f"  ✅ {name}")
            self.passed += 1
            return True
        else:
            print(f"  ❌ {name} NO ENCONTRADO")
            self.failed += 1
            return False

    def check_dependencies(self):
        """Verifica que las dependencias estén instaladas"""
        print("\n📦 VERIFICANDO DEPENDENCIAS...")
        
        try:
            import jwt
            print("  ✅ PyJWT instalado")
            self.passed += 1
        except ImportError:
            print("  ❌ PyJWT no instalado (ejecutar: pip install PyJWT)")
            self.failed += 1

        try:
            import bcrypt
            print("  ✅ bcrypt instalado")
            self.passed += 1
        except ImportError:
            print("  ❌ bcrypt no instalado (ejecutar: pip install bcrypt)")
            self.failed += 1

        try:
            import psycopg2
            print("  ✅ psycopg2 instalado")
            self.passed += 1
        except ImportError:
            print("  ❌ psycopg2 no instalado (ejecutar: pip install psycopg2-binary)")
            self.failed += 1

    def check_backend_files(self):
        """Verifica archivos del backend"""
        print("\n🔐 VERIFICANDO BACKEND...")
        
        files = [
            (self.backend_path / "app/config/jwt_config.py", "jwt_config.py"),
            (self.backend_path / "app/controllers/auth_controller.py", "auth_controller.py"),
            (self.backend_path / "app/routes/auth_routes.py", "auth_routes.py"),
            (self.backend_path / "app/sql/add_auth_fields.sql", "add_auth_fields.sql"),
            (self.backend_path / "app/sql/insert_test_users.sql", "insert_test_users.sql"),
            (self.backend_path / "requirements.txt", "requirements.txt"),
            (self.backend_path / "main.py", "main.py"),
        ]

        for path, name in files:
            self.check_file_exists(path, name)

    def check_frontend_files(self):
        """Verifica archivos del frontend"""
        print("\n🎨 VERIFICANDO FRONTEND...")
        
        files = [
            (self.frontend_path / "assets/scripts/auth.js", "auth.js"),
            (self.frontend_path / "assets/scripts/auth-guard.js", "auth-guard.js"),
            (self.frontend_path / "index.html", "index.html"),
            (self.frontend_path / "admin.html", "admin.html"),
            (self.frontend_path / "user.html", "user.html"),
            (self.frontend_path / "aiagent.html", "aiagent.html"),
        ]

        for path, name in files:
            self.check_file_exists(path, name)

    def check_database(self):
        """Verifica conexión a la base de datos"""
        print("\n🗄️  VERIFICANDO BASE DE DATOS...")
        
        try:
            import psycopg2
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                user="postgres",
                password="jklm212rich17",
                dbname="Database-CUL/CUC_0.0.1"
            )
            cursor = conn.cursor()
            
            # Verificar tabla personas
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name='personas' AND column_name='username'
            """)
            
            if cursor.fetchone():
                print("  ✅ Tabla personas tiene columna 'username'")
                self.passed += 1
            else:
                print("  ❌ Tabla personas NO tiene columna 'username' - ejecutar add_auth_fields.sql")
                self.warnings += 1
            
            # Verificar tabla tokens_activos
            cursor.execute("""
                SELECT 1 FROM information_schema.tables 
                WHERE table_name='tokens_activos'
            """)
            
            if cursor.fetchone():
                print("  ✅ Tabla tokens_activos existe")
                self.passed += 1
            else:
                print("  ⚠️  Tabla tokens_activos NO existe - ejecutar add_auth_fields.sql")
                self.warnings += 1
            
            # Contar usuarios
            cursor.execute("SELECT COUNT(*) FROM personas WHERE username IS NOT NULL")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"  ✅ {count} usuario(s) con username encontrado(s)")
                self.passed += 1
            else:
                print("  ⚠️  No hay usuarios creados - ejecutar insert_test_users.sql")
                self.warnings += 1
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"  ❌ Error conectando a BD: {e}")
            self.failed += 1

    def check_main_py(self):
        """Verifica que main.py importe auth_routes"""
        print("\n📝 VERIFICANDO main.py...")
        
        with open(self.backend_path / "main.py", "r") as f:
            content = f.read()
            
            if "auth_routes" in content:
                print("  ✅ main.py importa auth_routes")
                self.passed += 1
            else:
                print("  ❌ main.py NO importa auth_routes")
                self.failed += 1
            
            if "app.include_router(auth_router" in content:
                print("  ✅ auth_router incluido en main.py")
                self.passed += 1
            else:
                print("  ❌ auth_router NO incluido en main.py")
                self.failed += 1

    def check_html_files(self):
        """Verifica que HTML incluya scripts de auth"""
        print("\n🌐 VERIFICANDO HTML FILES...")
        
        html_files = [
            (self.frontend_path / "index.html", "index.html"),
            (self.frontend_path / "admin.html", "admin.html"),
        ]

        for path, name in html_files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
                if "auth.js" in content:
                    print(f"  ✅ {name} incluye auth.js")
                    self.passed += 1
                else:
                    print(f"  ❌ {name} NO incluye auth.js")
                    self.failed += 1

    def show_summary(self):
        """Muestra resumen de verificaciones"""
        print("\n" + "="*50)
        print("RESUMEN DE VERIFICACIÓN")
        print("="*50)
        
        total = self.passed + self.failed + self.warnings
        
        print(f"✅ Pasadas:    {self.passed}/{total}")
        print(f"❌ Fallidas:   {self.failed}/{total}")
        print(f"⚠️  Advertencias: {self.warnings}/{total}")
        
        if self.failed == 0 and self.warnings == 0:
            print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
            print("Listo para iniciar el sistema JWT")
            return True
        elif self.failed == 0:
            print(f"\n✅ Sistema listo (con {self.warnings} advertencia(s))")
            return True
        else:
            print(f"\n❌ Hay {self.failed} error(es) que corrija antes de iniciar")
            return False

    def run(self):
        """Ejecuta todas las verificaciones"""
        print("="*50)
        print("VERIFICACIÓN DE JWT IMPLEMENTATION")
        print("="*50)
        
        self.check_backend_files()
        self.check_frontend_files()
        self.check_dependencies()
        self.check_main_py()
        self.check_html_files()
        self.check_database()
        
        success = self.show_summary()
        
        print("\n📖 PRÓXIMOS PASOS:")
        print("1. python main.py (iniciar backend)")
        print("2. start start_frontend.bat (iniciar frontend)")
        print("3. Ingresar con usuario: admin / contraseña: admin123")
        
        return 0 if success else 1

if __name__ == "__main__":
    checker = JWTChecklist()
    sys.exit(checker.run())
