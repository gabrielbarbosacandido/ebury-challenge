#!/bin/bash
source scripts/project_config.sh 

# Function to check if the image exists locally and pull it if not
build_airflow_image() {
    if ! docker image inspect "$AIRFLOW_IMAGE_URI" > /dev/null 2>&1; then
        echo "Building the Airflow image..."
        docker pull "$AIRFLOW_IMAGE_URI"
    else
        echo "Image $AIRFLOW_IMAGE_URI is already installed."
    fi
}

# Function to start the Airflow service using Docker Compose
start_airflow() {
    build_airflow_image
    echo "Starting Airflow..."
    docker-compose -f docker-compose.yaml up -d
}

# Function to stop the Airflow service
stop_airflow() {
    echo "Stopping Airflow..."
    docker-compose -f docker-compose.yaml down -v
}

# Main function to handle the chosen task
main() {
    local func="$1"
    
    case "$func" in
        build_airflow_image)
            build_airflow_image
            ;;
        start_airflow)
            start_airflow
            ;;
        stop_airflow)
            stop_airflow
            ;;
        *)
            echo "Function not found: $func"
            exit 1
            ;;
    esac
}

main "$1"
