# Caminho: infra/main.tf

##############################################
# 1️⃣ ECR Repository: Armazena as imagens Docker
##############################################
#resource "aws_ecr_repository" "app_repo" {
#  name                 = var.app_name
#  image_tag_mutability = "MUTABLE"
#
#  lifecycle {
#    prevent_destroy = false
#  }
#}

##############################################
# 2️⃣ ECS Cluster: Onde as tasks vão rodar
##############################################
resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.app_name}-cluster"
}

##############################################
# 3️⃣ Security Group: Libera porta 8000 para acesso externo
##############################################
#resource "aws_security_group" "app_sg" {
#  name        = "${var.app_name}-sg"
#  description = "Allow inbound traffic on app port"
#  vpc_id      = data.aws_vpc.default.id
#
#  ingress {
#    from_port   = var.container_port
#    to_port     = var.container_port
#    protocol    = "tcp"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#
#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#}

##############################################
# 4️⃣ IAM Role para ECS Task Execution
##############################################
#resource "aws_iam_role" "ecs_task_execution_role" {
#  name = "${var.app_name}-ecs-task-execution-role"
#
#  assume_role_policy = jsonencode({
#    Version = "2012-10-17"
#    Statement = [
#      {
#        Action = "sts:AssumeRole"
#        Effect = "Allow"
#        Principal = {
#          Service = "ecs-tasks.amazonaws.com"
#        }
#      }
#    ]
#  })
#}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

##############################################
# 5️⃣ ECS Task Definition (imagem será atualizada no pipeline)
##############################################
resource "aws_ecs_task_definition" "app_task" {
  family                   = "${var.app_name}-task"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = var.app_name
      image     = "${aws_ecr_repository.app_repo.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]
    }
  ])
}

##############################################
# 6️⃣ ECS Service: Executando no Fargate sem LB
##############################################
resource "aws_ecs_service" "app_service" {
  name            = "${var.app_name}-service"
  cluster         = aws_ecs_cluster.app_cluster.id
  task_definition = aws_ecs_task_definition.app_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets         = data.aws_subnets.default.ids
    security_groups = [aws_security_group.app_sg.id]
    assign_public_ip = true
  }
}

##############################################
# 7️⃣ Data Sources: VPC & Subnets default
##############################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
