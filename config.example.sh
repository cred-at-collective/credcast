#!/bin/bash

# Server configuration
# Copy this file to config.sh and edit with your details

# Your Digital Ocean server IP or hostname
export CREDCAST_SERVER="root@YOUR_DIGITAL_OCEAN_IP"

# Remote path template - use {site_name} as a placeholder
export CREDCAST_REMOTE_PATH="/var/www/{site_name}"

# Default site name if not specified
export CREDCAST_DEFAULT_SITE="lux.cred.at"
