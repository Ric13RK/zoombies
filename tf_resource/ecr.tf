resource "aws_ecr_repository" "ml" {
  #tfsec:ignore:AWS093
  name                 = var.ecr_ml_repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}