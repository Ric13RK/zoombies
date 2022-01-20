provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Owner     = "Rishi"
      Team      = "Zoombies"
      CreatedBy = "Rishi"
    }
  }
}