output "ecr_repository_url" {
  value       = aws_ecr_repository.worker.repository_url
  description = "ECR repository URL for the worker image."
}

output "frontend_bucket_name" {
  value       = aws_s3_bucket.frontend.bucket
  description = "Bucket name for the static frontend."
}

output "frontend_website_url" {
  value       = "http://${aws_s3_bucket_website_configuration.frontend.website_endpoint}"
  description = "Public website URL for the static frontend bucket."
}

output "lambda_function_url" {
  value       = aws_lambda_function_url.api.function_url
  description = "Base URL for the Lambda control plane."
}

output "ecs_cluster_arn" {
  value       = aws_ecs_cluster.main.arn
  description = "ECS cluster ARN."
}

output "ecs_task_definition_arn" {
  value       = aws_ecs_task_definition.worker.arn
  description = "Task definition ARN used for each solve request."
}
