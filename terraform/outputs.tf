###########################################################################
# Outputs
###########################################################################
output "region" {
  description = "IBM Cloud region used"
  value       = var.region
}

output "resource_group_id" {
  description = "ID of the resource group"
  value       = data.ibm_resource_group.resource_group.id
}

output "project_id" {
  description = "Code Engine project ID"
  value       = ibm_code_engine_project.code_engine_project_instance.project_id
}

output "app_id" {
  description = "Code Engine app ID"
  value       = ibm_code_engine_app.code_engine_app_instance.id
}

output "app_name" {
  description = "Code Engine app name"
  value       = ibm_code_engine_app.code_engine_app_instance.name
}

output "app_url" {
  description = "Public URL of the app (when created with a public endpoint)"
  value       = ibm_code_engine_app.code_engine_app_instance.endpoint
}