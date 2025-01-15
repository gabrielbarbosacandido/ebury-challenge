#!/bin/bash
source scripts/project_config.sh 

build_airflow_image() {
    if ! docker image inspect "$AIRFLOW_IMAGE_URI" > /dev/null 2>&1; then
        echo "Construindo a imagem do Airflow..."
        docker build -t "$AIRFLOW_IMAGE_URI" -f Dockerfile .
    else
        echo "Imagem $AIRFLOW_IMAGE_URI já está instalada."
    fi
}

start_airflow() {
    build_airflow_image
    echo "Iniciando o Airflow..."
    docker-compose -f docker-compose.yaml up -d
}

stop_airflow() {
    echo "Parando o Airflow..."
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
            echo "Função não encontrada: $func"
            exit 1
            ;;
    esac
}

main "$1"
