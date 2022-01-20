resource "aws_ecs_cluster" "ml_batch" {
  name = var.ecs_cluster_name

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  #tfsec:ignore:AWS089
  name              = "/ecs/${var.ecs_cluster_name}-${var.ecr_ml_repo_name}"
  retention_in_days = 0
}

resource "aws_ecs_task_definition" "qna_ml_batch_algo_x" {
  family                   = "${var.ecr_ml_repo_name}-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name : var.ecr_ml_repo_name,
      image : "${aws_ecr_repository.ml.repository_url}:latest",
      essential : true,
      environment : [
        {
          name : "ENV_NAME",
          value : "ENV_VAL"
        },
      ],
      logConfiguration : {
        logDriver : "awslogs",
        options : {
          awslogs-group : aws_cloudwatch_log_group.ecs_logs.name,
          awslogs-region : var.region,
          awslogs-stream-prefix : "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "app" {
  name            = var.ecr_ml_repo_name
  cluster         = aws_ecs_cluster.ml_batch.id
  launch_type     = "FARGATE"
  task_definition = aws_ecs_task_definition.qna_ml_batch_algo_x.arn
  # desired_count   = var.replicas

  network_configuration {
    security_groups = ["sg-08eb06c89f9de80e7", "sg-0bddb5e342fa06651"]
    subnets = [
      "subnet-0bacbf530f2eadf33",
      "subnet-008faf56519281544",
      "subnet-0a7f90b9cf3559fc4"
    ]
  }

  #   load_balancer {
  #     target_group_arn = 
  #     container_name   = 
  #     container_port   = 
  #   }

  enable_ecs_managed_tags = true
  propagate_tags          = "SERVICE"

  #   # workaround for https://github.com/hashicorp/terraform/issues/12634
  #   depends_on = [aws_alb_listener.RESOURCE_NAME]

  #   # [after initial apply] don't override changes made to task_definition
  #   # from outside of terraform (i.e.; fargate cli)
  #   lifecycle {
  #     ignore_changes = [task_definition]
  #   }
}