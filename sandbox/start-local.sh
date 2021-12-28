aws configure --profile sandbox        
      
export AWS_DEFAULT_PROFILE=sandbox     
pulumi stack init  
pulumi config set aws:profile sandbox
pulumi config set aws:region us-east-1

# pulumi stack rm --force