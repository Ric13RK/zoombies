variable "region" {
  type        = string
  default     = "ap-southeast-2"
  description = "AWS Region"
}


variable "ecr_ml_repo_name" {
  type        = string
  default     = "qna-ml-algo-x"
  description = "ECR repositery name"
}

variable "ecs_cluster_name" {
  type        = string
  default     = "zoombies"
  description = "ECS cluster name"
}