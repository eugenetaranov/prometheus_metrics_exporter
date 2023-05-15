# Prometheus Metrics Exporter

The Prometheus Metrics Exporter is a service that periodically retrieves aggregated metric values from Prometheus and pushes them to CloudWatch. It is designed to run as a cronjob, allowing you to regularly sync your Prometheus metrics with CloudWatch for monitoring and analysis.

## Features

- Periodically fetches aggregated metric values from Prometheus
- Pushes the metrics to CloudWatch for monitoring and analysis
- Configurable scheduling intervals to suit your needs

## Prerequisites

Before running the Prometheus Metrics Exporter, ensure the following prerequisites are met:

- Prometheus server is accessible and properly configured.
- AWS credentials are set up for the environment where the exporter will run.
- CloudWatch metrics namespace and permissions are properly configured.

## Installation

1. Clone the Prometheus Metrics Exporter repository.
2. Install the required dependencies using the package manager of your choice.
3. Configure the exporter by updating the configuration file with your Prometheus and CloudWatch settings.
4. Set up the cronjob to execute the exporter at the desired intervals.
5. Start the cronjob, and the exporter will begin syncing metrics from Prometheus to CloudWatch.

## Configuration

The Prometheus Metrics Exporter configuration file (`config.yaml`) contains the necessary settings for connecting to Prometheus and CloudWatch. Update the following parameters according to your environment:

- `prometheus_url`: The URL of your Prometheus server.
- `cloudwatch_namespace`: The CloudWatch namespace where the metrics will be pushed.
- `metrics`: List of Prometheus metrics to be synced with CloudWatch.

## Usage

1. Run the Prometheus Metrics Exporter as a cronjob with the desired scheduling interval.
2. The exporter will connect to the configured Prometheus server and retrieve the aggregated metric values.
3. The metrics will be pushed to the specified CloudWatch namespace for monitoring and analysis.

## Troubleshooting

- If the exporter fails to connect to Prometheus or encounters any issues during the synchronization process, check the logs for error messages and ensure the configuration settings are correct.
- Verify that the AWS credentials and CloudWatch permissions are properly configured to allow the exporter to push metrics to CloudWatch.

## Contributing

Contributions are welcome! If you find any bugs, have suggestions, or would like to add new features, please open an issue or submit a pull request.

## License

The Prometheus Metrics Exporter is released under the [MIT License](LICENSE). You are free to use, modify, and distribute the software as per the terms of the license.
