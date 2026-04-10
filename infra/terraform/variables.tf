variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Base name used across resources."
  type        = string
  default     = "wordle-solver"
}

variable "environment" {
  description = "Environment suffix for resource naming."
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR range for the lightweight public VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "worker_image_uri" {
  description = "Full ECR image URI for the ECS worker."
  type        = string
  default     = ""
}

variable "lambda_zip_path" {
  description = "Path to the prebuilt Lambda zip artifact."
  type        = string
  default     = "../../dist/lambda/wordle-solver-lambda.zip"
}

variable "frontend_bucket_name" {
  description = "Optional explicit name for the static frontend bucket."
  type        = string
  default     = ""
}

variable "result_bucket_name" {
  description = "Optional explicit name for the short-lived result bucket."
  type        = string
  default     = ""
}

variable "worker_cpu" {
  description = "CPU units for the Fargate worker task."
  type        = number
  default     = 256
}

variable "worker_memory" {
  description = "Memory in MiB for the Fargate worker task."
  type        = number
  default     = 512
}

variable "lambda_timeout_seconds" {
  description = "Timeout for the Lambda control plane."
  type        = number
  default     = 90
}

variable "solver_wait_timeout_seconds" {
  description = "How long Lambda waits for the ECS task to finish."
  type        = number
  default     = 60
}
