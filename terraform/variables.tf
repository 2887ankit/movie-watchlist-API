###################################################################
# Input Variables
###################################################################
variable "region" {
  description = "IBM Cloud region"
  type        = string
  default     = "eu-gb"
}

variable "resource_group" {
  description = "Existing IBM Cloud resource group name"
  type        = string
  default     = "Default"
}

variable "project_name" {
  description = "Code Engine project name"
  type        = string
  default     = "movie-watchlist-project"
}

variable "app_name" {
  description = "Code Engine app name"
  type        = string
  default     = "movie-watchlist"
}

variable "image_reference" {
  description = "The name of the public image that is used for the app."
  type        = string
}

variable "image_port" {
  description = "The port which is used to connect to the port that is exposed by the container image."
  type        = number
  default     = 8080
}

variable "scale_cpu_limit" {
  description = "The number of CPU set for the instance of the app."
  type        = string
  default     = "0.25"
}

variable "scale_memory_limit" {
  description = "The amount of memory set for the instance of the app."
  type        = string
  default     = "0.5G"
}

variable "scale_min_instances" {
  description = "The minimum number of instances for this app.  If you set this value to 0, the app will scale down to zero, if not hit by any request for some time.)"
  type        = number
  default     = 0
}

variable "scale_max_instances" {
  description = "The maximum number of instances for this app."
  type        = number
  default     = 1
}

variable "database_url" {
  description = "DATABASE_URL environment variable (SQLite by default)"
  type        = string
  default     = "sqlite:///./movies.db"
}