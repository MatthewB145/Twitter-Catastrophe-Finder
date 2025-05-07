FROM public.ecr.aws/lambda/python:3.13

# Copy all contents of the current directory to the Lambda task root
COPY . ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Set the Lambda handler (filename.function)
CMD ["classify_posts.lambda_handler"]