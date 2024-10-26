#!/bin/bash

# Archivo final donde se guardarán las contraseñas finales
output_file="passwords_cracked_foromotos.txt"

> "$output_file"

temp_file=$(mktemp)

john --format=RAW-MD5 --wordlist=/wordlists/languages/spanish.txt --rules g22_foromotos.txt
john --show --format=RAW-MD5 g22_foromotos.txt | grep ':' >> "$temp_file"

john --format=RAW-MD5 --incremental --fork=3 g22_foromotos.txt --min-length=4 --max-length=5
john --show --format=RAW-MD5 g22_foromotos.txt | grep ':' >> "$temp_file"

john --format=RAW-MD5 --wordlist=/wordlists/languages/spanish.txt --rules=appendnumbers_and_specials_simple --max-run-time=100 g22_foromotos.txt
john --show --format=RAW-MD5 g22_foromotos.txt | grep ':' >> "$temp_file"

john --format=RAW-MD5 --wordlist=/wordlists/languages/spanish.txt --rules=MyRule g22_foromotos.txt
john --show --format=RAW-MD5 g22_foromotos.txt | grep ':' >> "$temp_file"

john --format=RAW-MD5 --incremental --fork=5 --min-length=6 --max-length=6 --max-run-time=1320 g22_foromotos.txt
john --show --format=RAW-MD5 g22_foromotos.txt | grep ':' >> "$temp_file"

sort -u "$temp_file" > "$output_file"

rm "$temp_file"

# Fin del script
