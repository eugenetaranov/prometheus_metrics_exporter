#!/usr/bin/env python
import os

import boto3
import botocore
import yaml
from prometheus_api_client import PrometheusConnect
from loguru import logger


def read_config(file_path: str) -> dict:
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    return config


class PrometheusMetrics:
    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url
        self.prometheus_api = PrometheusConnect(url=self.prometheus_url)

    def list_metrics(self, prefix: str = None) -> list[str]:
        try:
            metrics = self.prometheus_api.all_metrics()

            if prefix:
                metrics = [metric for metric in metrics if metric.startswith(prefix)]
                logger.info(f"Discovered {len(metrics)} metrics with prefix '{prefix}'")
            else:
                logger.info(f"Discovered {len(metrics)} metrics")

            return metrics
        except Exception as e:
            logger.error(f"Error listing metrics: {e}")

        return []

    def fetch_metric_values(self, metric: str) -> list[str]:
        try:
            values = self.prometheus_api.get_current_metric_value(metric_name=metric)
            logger.info(f"Found {len(values)} values for metric '{metric}'")
            return values

        except Exception as e:
            logger.error(
                f"Error fetching values for metric '{metric}' from Prometheus API: {e}"
            )

        return []

    def fetch_metric_aggregated(self, metric: str, aggregation: str) -> list[str]:
        try:
            values = self.prometheus_api.get_metric_aggregation(
                query=metric, operations=[aggregation]
            )
            logger.info(f"Found {len(values)} values for metric '{metric}'")
            return values

        except Exception as e:
            logger.error(
                f"Error fetching values for metric '{metric}' from Prometheus API: {e}"
            )

        return []


class CloudWatchMetrics:
    def __init__(self, region: str):
        self.cloudwatch = boto3.client(
            "cloudwatch",
            region_name=region,
            config=botocore.config.Config(retries={"max_attempts": 10}),
        )

    def write_metric(
        self, namespace: str, dimensions: list[dict], metric_name: str, value: float
    ) -> bool:
        try:
            res = self.cloudwatch.put_metric_data(
                Namespace=namespace,
                MetricData=[
                    {
                        "MetricName": metric_name,
                        "Dimensions": dimensions,
                        "Unit": "Count",
                        "Value": value,
                    },
                ],
            )

        except Exception as e:
            logger.error(f"Error writing metric '{metric_name}' to CloudWatch: {e}")
            return False

        if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True

        return False


def main():
    logger.info("Starting Prometheus Metrics Fetcher")
    config_path = os.environ.get("CONFIG_FILE", "config.yaml")
    region = os.environ.get("AWS_REGION")
    k8s_cluster = os.environ.get("K8S_CLUSTER")
    prometheus_url = os.environ.get("PROMETHEUS_ENDPOINT")
    cfg = {}

    try:
        cfg = read_config(config_path)
        logger.info(f"Loaded config from {config_path}")
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {e}")
        exit(1)

    logger.debug(f"Config: {cfg}")

    pm = PrometheusMetrics(prometheus_url=prometheus_url)
    cw = CloudWatchMetrics(region=region)

    for metric in cfg["metrics"]:
        aggregated_value = int(
            pm.fetch_metric_aggregated(
                metric=metric["name"], aggregation=metric["aggregation"]
            )[metric["aggregation"]]
        )
        logger.info(f"Metric '{metric['name']}' aggregated value: {aggregated_value}")

        res = cw.write_metric(
            namespace=cfg["cloudwatch_namespace"],
            metric_name=metric["name"],
            value=aggregated_value,
            dimensions=[
                {
                    "Name": "k8s_cluster",
                    "Value": k8s_cluster,
                },
            ],
        )

        if res:
            logger.info(
                f"Metric '{cfg['cloudwatch_namespace']}/{metric['name']}:{aggregated_value}' was written to CloudWatch"
            )
        else:
            exit(1)


if __name__ == "__main__":
    main()
