#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para generar hashes bcrypt para contraseñas JWT
Uso: python generate_password_hash.py
"""

import bcrypt
import sys

def generate_hash(password):
    """Genera un hash bcrypt para una contraseña"""
    salt = bcrypt.gensalt(rounds=12)
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')

def verify_hash(password, hash_str):
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_str.encode('utf-8'))

def main():
    print("=" * 60)
    print("Generador de Hashes Bcrypt para JWT")
    print("=" * 60)
    
    while True:
        print("\nOpciones:")
        print("1. Generar hash de una contraseña")
        print("2. Verificar contraseña contra hash")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            contraseña = input("Ingrese la contraseña a hashear: ").strip()
            if not contraseña:
                print("Error: La contraseña no puede estar vacía")
                continue
            
            hash_resultado = generate_hash(contraseña)
            print("\nHash generado:")
            print(f"   Contraseña: {contraseña}")
            print(f"   Hash: {hash_resultado}")
            print("\nUse este hash en la BD:")
            print("   INSERT INTO personas (nombre, documento, correo, username, password_hash, id_rol, estado)")
            print(f"   VALUES ('Nombre', 'Doc', 'email@univ.edu', 'username', '{hash_resultado}', 1, 1);")
            
        elif opcion == "2":
            contraseña = input("Ingrese la contraseña a verificar: ").strip()
            hash_str = input("Ingrese el hash: ").strip()
            
            if verify_hash(contraseña, hash_str):
                print("La contraseña coincide con el hash")
            else:
                print("La contraseña NO coincide con el hash")
        
        elif opcion == "3":
            print("Hasta luego!")
            break
        
        else:
            print("Opción no válida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
