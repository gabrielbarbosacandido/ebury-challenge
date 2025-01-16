#!/bin/bash
source scripts/project_config.sh 


build_airflow_image() {
    if ! docker image inspect "$AIRFLOW_IMAGE_URI" > /dev/null 2>&1; then
        echo "Building the Airflow image..."
        docker pull "$AIRFLOW_IMAGE_URI"
    else
        echo "Image $AIRFLOW_IMAGE_URI is already installed."
    fi
}


start_airflow() {
    build_airflow_image
    echo "Starting Airflow..."
    docker-compose -f docker-compose.yaml up -d
}


stop_airflow() {
    echo "Stopping Airflow..."
    docker-compose -f docker-compose.yaml down -v
}


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
