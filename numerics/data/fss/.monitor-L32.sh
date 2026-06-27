#!/bin/bash
# Monitor L=32 simulation process

PID=9595
CHECKPOINT="/Users/sage/.openclaw/workspace/code/timesarrow/numerics/data/fss/.checkpoint-L32-20260627-lean.json"
LOGFILE="/Users/sage/.openclaw/workspace/code/timesarrow/numerics/data/fss/t20-p3b-L32-lean-20260627.log"
MONITOR_LOG="/Users/sage/.openclaw/workspace/code/timesarrow/numerics/data/fss/.monitor-L32-20260627.log"

# Get initial log size
LAST_LOG_SIZE=$(wc -c < "$LOGFILE" 2>/dev/null || echo 0)
LAST_LOG_LINES=$(wc -l < "$LOGFILE" 2>/dev/null || echo 0)
LAST_CHECK_TIME=$(date +%s)
CHECKPOINT_FOUND=false
START_TIME=$(date +%s)

echo "=== Monitor started at $(date) ===" > "$MONITOR_LOG"
echo "PID: $PID" >> "$MONITOR_LOG"
echo "Initial log size: $LAST_LOG_SIZE bytes, $LAST_LOG_LINES lines" >> "$MONITOR_LOG"
echo "" >> "$MONITOR_LOG"

while true; do
    sleep 300  # 5 minutes
    
    NOW=$(date +%s)
    ELAPSED=$((NOW - START_TIME))
    ELAPSED_MIN=$((ELAPSED / 60))
    
    echo "--- Check at $(date) (elapsed: ${ELAPSED_MIN}m) ---" >> "$MONITOR_LOG"
    
    # Check if process is running
    if ps -p $PID > /dev/null 2>&1; then
        ps -p $PID -o pid,pcpu,pmem,etime,command >> "$MONITOR_LOG" 2>&1
        IS_RUNNING=true
    else
        echo "PID $PID NOT RUNNING" >> "$MONITOR_LOG"
        IS_RUNNING=false
    fi
    
    # Check checkpoint
    if [ -f "$CHECKPOINT" ]; then
        CKPT_SIZE=$(wc -c < "$CHECKPOINT")
        CKPT_LINES=$(wc -l < "$CHECKPOINT")
        echo "CHECKPOINT EXISTS: ${CKPT_SIZE} bytes, ${CKPT_LINES} lines" >> "$MONITOR_LOG"
        if [ "$CHECKPOINT_FOUND" = false ]; then
            echo "MILESTONE: FIRST CHECKPOINT CREATED" >> "$MONITOR_LOG"
            CHECKPOINT_FOUND=true
        fi
    else
        echo "NO CHECKPOINT" >> "$MONITOR_LOG"
    fi
    
    # Check log growth
    CURRENT_LOG_SIZE=$(wc -c < "$LOGFILE" 2>/dev/null || echo 0)
    CURRENT_LOG_LINES=$(wc -l < "$LOGFILE" 2>/dev/null || echo 0)
    SIZE_DELTA=$((CURRENT_LOG_SIZE - LAST_LOG_SIZE))
    LINES_DELTA=$((CURRENT_LOG_LINES - LAST_LOG_LINES))
    echo "LOG: ${CURRENT_LOG_SIZE} bytes (${SIZE_DELTA:+${SIZE_DELTA}}), ${CURRENT_LOG_LINES} lines (${LINES_DELTA:+${LINES_DELTA}})" >> "$MONITOR_LOG"
    
    # Check for progress
    if [ "$CURRENT_LOG_SIZE" -gt "$LAST_LOG_SIZE" ]; then
        LAST_CHECK_TIME=$NOW
        echo "PROGRESS: Log grew by ${SIZE_DELTA} bytes, ${LINES_DELTA} lines" >> "$MONITOR_LOG"
    fi
    
    # Check for stall (no progress for 30 min)
    TIME_SINCE_PROGRESS=$((NOW - LAST_CHECK_TIME))
    if [ "$TIME_SINCE_PROGRESS" -ge 1800 ]; then
        echo "ALERT: NO PROGRESS FOR $((TIME_SINCE_PROGRESS / 60)) MINUTES" >> "$MONITOR_LOG"
    fi
    
    # Check log for completion markers
    if [ -f "$LOGFILE" ]; then
        if grep -q "All betas completed\|Completed all\|Final results\|Done" "$LOGFILE" 2>/dev/null; then
            echo "MILESTONE: COMPLETION DETECTED IN LOG" >> "$MONITOR_LOG"
        fi
    fi
    
    LAST_LOG_SIZE=$CURRENT_LOG_SIZE
    LAST_LOG_LINES=$CURRENT_LOG_LINES
    echo "" >> "$MONITOR_LOG"
    
    # Exit if process is done
    if [ "$IS_RUNNING" = false ]; then
        echo "Process ended at $(date)" >> "$MONITOR_LOG"
        break
    fi
done

echo "=== Monitor ended at $(date) ===" >> "$MONITOR_LOG"
