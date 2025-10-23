# Caminho: infra/outputs.tf

output "ecr_repository_url" {
  description = "URL do repositório ECR"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "ecs_cluster_name" {
  description = "Nome do cluster ECS"
  value       = aws_ecs_cluster.app_cluster.name
}

output "ecs_service_name" {
  description = "Nome do serviço ECS"
  value       = aws_ecs_service.app_service.name
}

output "task_definition_arn" {
  description = "ARN da task definition"
  value       = aws_ecs_task_definition.app_task.arn
}

output "security_group_id" {
  description = "ID do Security Group usado pelo serviço"
  value       = aws_security_group.app_sg.id
}
