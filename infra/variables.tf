# Caminho: infra/variables.tf

variable "aws_region" {
  description = "Região AWS para os recursos"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Nome base do aplicativo (usado em ECR, ECS Task, etc)"
  type        = string
  default     = "titanic-api"
}

variable "cpu" {
  description = "Quantidade de CPU para a task (em unidades ECS)"
  type        = string
  default     = "256" # equivalente a 0.25 vCPU
}

variable "memory" {
  description = "Memória para a task (em MiB)"
  type        = string
  default     = "512"
}

variable "container_port" {
  description = "Porta do container exposta pela aplicação FastAPI"
  type        = number
  default     = 8000
}
