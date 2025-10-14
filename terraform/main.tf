terraform {
  required_version = ">= 1.6.0"
  required_providers {
    ibm = {
      source = "IBM-Cloud/ibm"
      version = ">= 1.83.0"
    }
  }
}

# Configure the IBM Provider
provider "ibm" {
  region = var.region
}

# Code Engine project (logical namespace)
data "ibm_resource_group" "resource_group" {
  name = var.resource_group
}

resource "ibm_code_engine_project" "code_engine_project_instance" {
  name              = var.project_name
  resource_group_id = data.ibm_resource_group.resource_group.id
}

# Code Engine app (serverless container)
resource "ibm_code_engine_app" "code_engine_app_instance" {
  project_id      = ibm_code_engine_project.code_engine_project_instance.project_id
  name            = var.app_name
  image_reference = var.image_reference
  image_port      = var.image_port
  

  scale_cpu_limit    = var.scale_cpu_limit
  scale_memory_limit = var.scale_memory_limit

  scale_min_instances = var.scale_min_instances       
  scale_max_instances = var.scale_max_instances

  run_env_variables {
    name  = "DATABASE_URL"
    value = var.database_url
  }
}