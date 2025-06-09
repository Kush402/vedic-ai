#!/bin/bash

# Create ephe directory
mkdir -p backend/astrology/ephe

# Download Swiss Ephemeris files
cd backend/astrology/ephe

# Function to download file with retries
download_file() {
    local url=$1
    local output=$2
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        echo "Downloading $output (attempt $((retry_count + 1))/$max_retries)..."
        if curl -L -f "$url" -o "$output" --retry 3 --retry-delay 2; then
            if [ -s "$output" ] && ! grep -q "<html" "$output"; then
                echo "Successfully downloaded $output"
                return 0
            else
                echo "Downloaded file appears to be invalid, retrying..."
                rm -f "$output"
            fi
        fi
        retry_count=$((retry_count + 1))
        sleep 2
    done
    
    echo "Failed to download $output after $max_retries attempts"
    return 1
}

# Download files from a more reliable source
download_file "https://raw.githubusercontent.com/astrorigin/swisseph/master/ephe/sepl_18.se1" "sepl_18.se1"
download_file "https://raw.githubusercontent.com/astrorigin/swisseph/master/ephe/semo_18.se1" "semo_18.se1"
download_file "https://raw.githubusercontent.com/astrorigin/swisseph/master/ephe/seas_18.se1" "seas_18.se1"

# Verify files were downloaded and are valid
echo "Verifying downloaded files..."
for file in *.se1; do
    if [ -f "$file" ] && [ -s "$file" ] && ! grep -q "<html" "$file"; then
        echo "✓ $file is valid"
    else
        echo "✗ $file is invalid or missing"
        exit 1
    fi
done

echo "All files downloaded and verified successfully" 