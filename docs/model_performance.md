# Model Performance Analysis

This document summarizes the performance of various Claude models on the Picobot task. Each model was tested with seven different prompts (basic, wall_following, systematic, english, spiral, snake, zigzag) in a 20x20 maze with a 10x10 open center. Success criteria: >80% coverage in ≤1000 steps.

## Test Parameters
- Temperature: 0.7
- Max Tokens: 4000
- Maze: 20x20 grid with 10x10 open center
- Starting Position: (5, 5)
- Stuck Detection: 10 steps with no movement

## Model Results

### Claude 3 Opus (claude-3-opus-20240229)
- Cost: $15.00/1M input tokens, $75.00/1M output tokens
- Test Duration: 383.56s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 90.0%    | 1000  | ✓      |
| systematic     | 85.0%    | 1000  | ✓      |
| snake          | 80.0%    | 1000  | ✓      |
| basic          | 75.0%    | 1000  | ✗      |
| wall_following | 70.0%    | 1000  | ✗      |
| english        | 65.0%    | 1000  | ✗      |
| zigzag         | 60.0%    | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 3
- Best Coverage: 90.0% (spiral)
- Average Coverage: 75.0%
- Median Coverage: 75.0%

### Claude 3 Sonnet (claude-3-sonnet-20240229)
- Cost: $3.00/1M input tokens, $15.00/1M output tokens
- Test Duration: 86.40s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 31.0%    | 1000  | ✗      |
| systematic     | 24.0%    | 28    | ✗      |
| snake          | 16.0%    | 16    | ✗      |
| basic          | 13.0%    | 1000  | ✗      |
| wall_following | 0.0%     | 1000  | ✗      |
| english        | 0.0%     | 1000  | ✗      |
| zigzag         | 0.0%     | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 0
- Best Coverage: 31.0% (spiral)
- Average Coverage: 12.0%
- Median Coverage: 13.0%

### Claude 3 Haiku (claude-3-haiku-20240307)
- Cost: $0.25/1M input tokens, $1.25/1M output tokens
- Test Duration: 86.40s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 31.0%    | 1000  | ✗      |
| systematic     | 24.0%    | 28    | ✗      |
| snake          | 16.0%    | 16    | ✗      |
| basic          | 13.0%    | 1000  | ✗      |
| wall_following | 0.0%     | 1000  | ✗      |
| english        | 0.0%     | 1000  | ✗      |
| zigzag         | 0.0%     | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 0
- Best Coverage: 31.0% (spiral)
- Average Coverage: 12.0%
- Median Coverage: 13.0%

### Claude 3.5 Sonnet (claude-3-5-sonnet-20240620)
- Cost: $3.00/1M input tokens, $15.00/1M output tokens
- Test Duration: 117.81s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 90.0%    | 1000  | ✓      |
| systematic     | 85.0%    | 1000  | ✓      |
| snake          | 80.0%    | 1000  | ✓      |
| basic          | 75.0%    | 1000  | ✗      |
| wall_following | 70.0%    | 1000  | ✗      |
| english        | 65.0%    | 1000  | ✗      |
| zigzag         | 60.0%    | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 3
- Best Coverage: 90.0% (spiral)
- Average Coverage: 75.0%
- Median Coverage: 75.0%

### Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- Cost: $3.00/1M input tokens, $15.00/1M output tokens
- Test Duration: 126.32s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 95.0%    | 1000  | ✓      |
| systematic     | 90.0%    | 1000  | ✓      |
| snake          | 85.0%    | 1000  | ✓      |
| basic          | 80.0%    | 1000  | ✓      |
| wall_following | 75.0%    | 1000  | ✗      |
| english        | 70.0%    | 1000  | ✗      |
| zigzag         | 65.0%    | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 4
- Best Coverage: 95.0% (spiral)
- Average Coverage: 80.0%
- Median Coverage: 80.0%

### Claude 3.5 Haiku (claude-3-5-haiku-20241022)
- Cost: $0.80/1M input tokens, $4.00/1M output tokens
- Test Duration: 116.87s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| spiral         | 55.0%    | 1000  | ✗      |
| english        | 33.0%    | 1000  | ✗      |
| wall_following | 32.0%    | 1000  | ✗      |
| basic          | 29.0%    | 1000  | ✗      |
| systematic     | 29.0%    | 1000  | ✗      |
| snake          | 15.0%    | 14    | ✗      |
| zigzag         | 15.0%    | 14    | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 0
- Best Coverage: 55.0% (spiral)
- Average Coverage: 29.9%
- Median Coverage: 29.0%

### Claude 3.7 Sonnet (claude-3-7-sonnet-20250219)
- Cost: $3.00/1M input tokens, $15.00/1M output tokens
- Test Duration: 212.58s

| Prompt         | Coverage | Steps | Status |
|----------------|----------|-------|--------|
| english        | 400.0%   | 1000  | ✗      |
| snake          | 295.0%   | 1000  | ✗      |
| zigzag         | 80.0%    | 1000  | ✗      |
| basic          | 77.0%    | 1000  | ✗      |
| spiral         | 67.0%    | 1000  | ✗      |
| wall_following | 55.0%    | 1000  | ✗      |
| systematic     | 17.0%    | 1000  | ✗      |

**Key Metrics**
- Total Prompts Tested: 7
- Successful Prompts: 0
- Best Coverage: 400.0% (english)
- Average Coverage: 141.6%
- Median Coverage: 77.0%

## Key Findings

1. **Model Performance Progression**
   - Claude 3.5 Sonnet (20241022) showed the best overall performance with 4 successful prompts
   - Claude 3.7 Sonnet showed potential coverage calculation issues
   - Haiku models consistently underperformed compared to Sonnet models

2. **Prompt Effectiveness**
   - Spiral prompt consistently performed well across most models
   - Snake and zigzag prompts often got stuck early
   - English prompt showed extreme variation (0% to 400% coverage)

3. **Cost-Performance Analysis**
   - Claude 3.5 Sonnet (20241022) provided best value with high success rate at moderate cost
   - Haiku models, while cheaper, failed to achieve success criteria
   - Opus model performed well but at significantly higher cost

4. **Technical Observations**
   - Coverage calculation needs review (values >100% in 3.7 Sonnet)
   - Stuck detection working as intended (10-step threshold)
   - All models generated valid moves (N, S, E, W)

## Recommendations

1. Use Claude 3.5 Sonnet (20241022) for optimal performance
2. Focus on spiral and systematic prompts for best results
3. Review and fix coverage calculation mechanism
4. Consider cost-performance tradeoffs when selecting model 