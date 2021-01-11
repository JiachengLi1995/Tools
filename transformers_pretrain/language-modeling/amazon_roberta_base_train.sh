CUDA_VISIBLE_DEVICES=3,4 python -m torch.distributed.launch \
    --nproc_per_node 2 run_mlm_wwm.py \
    --model_name_or_path roberta-base \
    --train_file ../../review_lm_pretrain/Amazon_Review_train.txt \
    --validation_file ../../review_lm_pretrain/Amazon_Review_dev.txt \
    --do_train \
    --do_eval \
    --fp16 \
    --per_device_train_batch_size 32 \
    --weight_decay 0.01 \
    --adam_beta2 0.98 \
    --adam_epsilon 1e-6 \
    --evaluation_strategy 'steps' \
    --logging_steps 5000 \
    --save_steps 20000 \
    --eval_steps 50000 \
    --output_dir ./tmp/roberta-base/

# CUDA_VISIBLE_DEVICES=5 python run_mlm_wwm.py \
#     --model_name_or_path roberta-base \
#     --train_file ../../review_lm_pretrain/Amazon_Review_train.txt \
#     --validation_file ../../review_lm_pretrain/Amazon_Review_dev.txt \
#     --do_train \
#     --do_eval \
#     --fp16 \
#     --per_device_train_batch_size 1024 \
#     --output_dir ./tmp/roberta-base/