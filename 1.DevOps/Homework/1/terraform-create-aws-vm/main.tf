resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"  # ID AMI образу для EC2 (залежить від регіону)
  instance_type = "t2.micro"  # Тип інстансу

  tags = {
    Name = "MyEC2Instance"
  }
}