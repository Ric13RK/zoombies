output "ecr_repository" {
  value       = aws_ecr_repository.ml
  description = "ECR Repo attributes reference"
}

output "ecs_cluster" {
  value       = aws_ecs_cluster.ml_batch
  description = "ECS cluster's attributes reference"
}

output "ecs_task_definition" {
  value       = aws_ecs_task_definition.qna_ml_batch_algo_x
  description = "ECS cluster's task defination attributes reference"
}