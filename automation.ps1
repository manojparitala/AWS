# Get all the SQL EC2 instances
$Instances = Get-EC2Instance -Filter @{Name = 'tag:Type'; Values = "SQL"}

# Get the current instance
$instanceId = Invoke-WebRequest -Uri http://169.254.169.254/latest/meta-data/instance-id -UseBasicParsing

# Get the instanceId's
$EC2Instances = $Instances.Instances
$a = $EC2Instances.InstanceId

# Get the Tags values
$tag_list = $EC2Instances.Tags.value -like "PRO*"
$b = $tag_list
$c = $b.Count

$arr += $a
$brr += $b

$hash = @{}
for ($i = 0; $i -lt $c; $i++)
{
  $hash.add($arr[$i], $brr[$i])
}

#echo $hash[$instanceId.Content]


# Constants
$sourceDrive = "C:\"
$sourceFolder = "MYSQL\Backup"
$sourcePath = $sourceDrive + $sourceFolder
$s3Bucket = "manojprobucket"

foreach ($instance in $a)
{
   if ($instance -eq $instanceId.Content)
   {
      $k = $hash[$instance]
$s3Folder = $k #e.g. PRO1

  # FUNCTION – Iterate through subfolders and upload files to S3
  function RecurseFolders([string]$path) {
    $fc = New-Object -com Scripting.FileSystemObject
    $folder = $fc.GetFolder($path)
    foreach ($i in $folder.SubFolders) {
      $thisFolder = $i.Path

      # Transform the local directory path to notation compatible with S3 Buckets and Folders
      # 1. Trim off the drive letter and colon from the start of the Path
      $s3Path = $thisFolder.ToString()
      $s3Path = $s3Path.SubString(2)
      # 2. Replace back-slashes with forward-slashes
      # Escape the back-slash special character with a back-slash so that it reads it literally, like so: "\\"
      $s3Path = $s3Path -replace "\\", "/"
      $s3Path = "/" + $s3Folder + $s3Path

      # Upload directory to S3
      Write-S3Object -BucketName $s3Bucket -Folder $thisFolder -KeyPrefix $s3Path
    }

    # If subfolders exist in the current folder, then iterate through them too
    foreach ($i in $folder.subfolders) {
      RecurseFolders($i.path)
    }
  }

  # Upload root directory files to S3
  $s3Path = "/" + $s3Folder + "/" + $sourceFolder
  Write-S3Object -BucketName $s3Bucket -Folder $sourcePath -KeyPrefix $s3Path

  # Upload subdirectories to S3
  RecurseFolders($sourcePath)
   }
}
