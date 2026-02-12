# my-local-ai-environment
An MCP server and tools I use for my local AI setup

## Usage

### Build the image if needed

`docker build -t my-local-ai-environment:latest .`

docker start -v <path to your files dir>:/mnt/data:rw --rm -p 8000:8000 my-local-ai-environment:latest