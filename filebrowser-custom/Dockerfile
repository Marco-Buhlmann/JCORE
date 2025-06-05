FROM filebrowser/filebrowser:latest

# Copy our startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Set the entrypoint to our custom script
ENTRYPOINT ["/start.sh"]
