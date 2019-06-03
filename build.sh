#!/bin/bash
set -e
codeBucket="bryanlabs-code"

declare -A profilemap
profilemap[myEnv]="BRYANLABS"

lambdalayers=(
    boto3cloudformation
)


# uncomment the resources you want to use
resources=(
    python/ramCreateResourceShare
    python/ec2CreateTransitGatewayRoute
    python/ec2CreateRoute
    python/ec2ZoneIds
    python/dsConnectDirectory
    python/dsShareDirectory
    python/dsAcceptSharedDirectory
)

for profile in "${!profilemap[@]}"
do
    echo ''
    echo Building for $profile ...

    for layer in "${lambdalayers[@]}"
    do
        : 
        # Configure Layers
        rm -rf lambdaLayers/$layer
        mkdir -p lambdaLayers/$layer/python/lib/python3.6/site-packages
        pip install -q --upgrade boto3 botocore cfn-resource crhelper -t lambdaLayers/$layer/python/lib/python3.6/site-packages/
        cd lambdaLayers/$layer
        zip -qr9 ../$layer.zip .
        cd ..
        aws --profile ${profilemap[$profile]} s3 cp --quiet $layer.zip s3://$codeBucket/
        layerversion="$(aws --profile ${profilemap[$profile]} s3api list-object-versions \
                --bucket $codeBucket \
                --prefix $layer.zip \
                | jq '.Versions[] | select(.IsLatest==true)' | jq -r .VersionId)"
        echo ${layer}ObjectVersion: $layerversion
        rm -rf $layer $layer.zip
        cd ..
    done

echo "Object Versions, Update templates / Parameters Accordingly."

    for resource in "${resources[@]}"
    do
        : 
        cd "$resource"
        codezip=$(basename $resource.zip)
        zip -qr9 $codezip .
        aws --profile ${profilemap[$profile]} s3 --quiet cp $codezip s3://$codeBucket/
        rm -rf $codezip
        version="$(aws --profile ${profilemap[$profile]} s3api list-object-versions \
        --bucket $codeBucket \
        --prefix $codezip \
        | jq '.Versions[] | select(.IsLatest==true)' | jq -r .VersionId)"
        cd ../..
        echo $(basename $resource)ObjectVersion: $version
    done
done