#!/bin/bash

# Deploy Frontend to S3 and Invalidate CloudFront Cache
# This script uploads frontend files to S3 and invalidates CloudFront cache

set -e

echo "🚀 Deploying Kiro Live Board Frontend"
echo "======================================"

# Get stack outputs
echo "📋 Getting stack outputs..."
API_URL=$(aws cloudformation describe-stacks --stack-name board-live-kiro --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name board-live-kiro --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' --output text)
CLOUDFRONT_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='CloudFront distribution for board-live-kiro Kiro Live Board'].Id" --output text)
CLOUDFRONT_DOMAIN=$(aws cloudformation describe-stacks --stack-name board-live-kiro --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDomain`].OutputValue' --output text)

echo "✅ API URL: $API_URL"
echo "✅ S3 Bucket: $BUCKET_NAME"
echo "✅ CloudFront Domain: $CLOUDFRONT_DOMAIN"

# Update API URLs in HTML files
echo ""
echo "🔧 Updating API URLs in frontend files..."
cd frontend
sed -i.bak "s|const API_URL = '.*';|const API_URL = '$API_URL';|g" registration.html
sed -i.bak "s|const API_BASE_URL = '.*';|const API_BASE_URL = '$API_URL';|g" board.html
rm -f *.bak

# Upload files to S3
echo ""
echo "📤 Uploading files to S3..."
aws s3 sync . s3://$BUCKET_NAME/ \
    --exclude "*.md" \
    --exclude "*.bak" \
    --exclude "test-*.html" \
    --cache-control "public, max-age=86400"

# Invalidate CloudFront cache
echo ""
echo "🔄 Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_ID \
    --paths "/*" \
    --query 'Invalidation.Id' \
    --output text

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📱 URLs:"
echo "   QR Screen (project this):    https://$CLOUDFRONT_DOMAIN/qr.html"
echo "   Registration Form:           https://$CLOUDFRONT_DOMAIN/registration.html"
echo "   Live Dashboard:              https://$CLOUDFRONT_DOMAIN/board.html"
echo ""
echo "⏳ CloudFront cache invalidation may take 1-2 minutes to complete"
