# Day 5 — Serving Models Your Way

## 1. Scenario

My scenario is a **college study assistant** running locally on my laptop. The assistant should explain programming and AI concepts in beginner-friendly language, use short examples when useful, avoid inventing facts when it is unsure, and keep answers clear and concise. The intended use is one student using the model locally for study.

I used Ollama with `qwen2.5:1.5b` as the base model because it is already installed locally and is small enough for my laptop. I created a custom Ollama model named `study-assistant`.

## 2. What is Ollama?

Ollama provides a local inference setup with three closely related parts: a background server, a command-line client, and a model library. The server loads a model and answers requests, normally through port 11434. The CLI provides commands such as `pull`, `run`, `list`, `ps`, `show`, and `create`. The model library provides ready-to-run model builds.

On Windows, Ollama model files are stored under the user's `.ollama\models` directory unless the model location is changed. In my scenario, a request is sent to the local Ollama server, the server loads or reuses `study-assistant`, the model generates tokens, and the response is returned to the Python program.

## 3. Modelfile

My Modelfile is:

```text
FROM qwen2.5:1.5b
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
SYSTEM "You are a friendly college study assistant..."
```

`FROM` chooses the base model. I used `qwen2.5:1.5b` because it is already available locally. `temperature 0.3` keeps responses relatively consistent. `num_ctx 4096` gives a practical context size for this laptop scenario. `SYSTEM` packages the desired study-assistant behaviour as the model's default instruction.

The custom model does not contain a second full copy of the neural-network weights. It is a customized model definition based on the existing base model, so `ollama create` did not need to download another copy of the model weights.

## 4. System prompt override

The Modelfile supplies the default behaviour. My Python OpenAI-compatible test supplies a different system prompt asking for a strict exam-answer style with exactly three bullet points. This demonstrates that an application can override the default behaviour when it needs a different instruction for a particular request. This is useful for agents because the application can keep a safe/default behaviour in the model while supplying task-specific instructions at runtime.

## 5. REST API

Ollama exposes its own REST API. I used `/api/generate` for direct prompt completion. A generate request contains a prompt and can be either streaming or non-streaming.

The `/api/chat` endpoint is designed around chat messages such as system, user and assistant roles. It is useful when conversation history matters.

Ollama also exposes an OpenAI-compatible endpoint under `/v1`. In my experiment, Python sent a `chat/completions` request to that endpoint. This matters because application code written against the OpenAI API shape can later be pointed at another compatible inference server, such as a vLLM deployment, by changing the server URL and model configuration.

## 6. Streaming, TTFT and total time

In a non-streaming request, the program waits for the complete response. In a streaming request, generated pieces are returned as soon as they are available.

**TTFT (Time To First Token)** is the time from sending the request until the first generated token/chunk is received. **Total time** is the elapsed time until the response is complete. Streaming can feel faster because the user sees the beginning of the answer earlier, even when the total generation time is similar.

The Python script records TTFT for the streaming request and total elapsed time for both styles. It also uses Ollama's reported evaluation count and evaluation duration to calculate tokens per second.

## 7. num_ctx, keep-alive and parallel requests

`num_ctx` controls the context window allocated for a request. A larger context can increase KV-cache memory, so it connects directly to the memory calculations from Day 4.

`OLLAMA_KEEP_ALIVE` controls how long a model stays loaded after a request. Keeping the model loaded can make repeated requests faster because the model does not need to be loaded again.

`OLLAMA_NUM_PARALLEL` controls how many requests can be processed in parallel. More parallel requests can improve concurrency, but they also increase memory pressure because multiple requests need runtime state and KV-cache capacity.

## 8. PagedAttention and prefix caching

The KV cache stores attention keys and values for tokens that have already been processed. A simple serving system can reserve memory in ways that leave fragmented or underused space as requests have different lengths.

PagedAttention manages KV-cache memory in fixed-size blocks and uses a block table to map logical token positions to physical blocks. This makes memory use more flexible and allows sharing of blocks when appropriate.

Prefix caching is especially useful for agents because many requests may repeat the same system prompt or long instruction prefix. Reusing the cached prefix avoids recomputing the same work for every request.

## 9. Static batching vs continuous batching

Static batching forms a batch of requests and processes that batch together. A request may wait for the current batch or for slower requests in that batch.

Continuous batching changes the scheduling dynamically. When one sequence finishes, another waiting sequence can be inserted into the running workload. This keeps the GPU more continuously occupied when many users are sending requests.

**Throughput** is the amount of work completed per unit time. **TTFT** is time to first token. **TPOT/ITL** is time per output token after the first token. **P95 latency** is the latency below which 95% of requests finish. Increasing concurrency and throughput can increase queueing or per-request latency, so deployment tuning is a trade-off rather than maximizing one metric blindly.

## 10. Ollama vs vLLM

| Basis | Ollama | vLLM |
|---|---|---|
| Built for | Local development and small-scale use | High-concurrency production serving |
| Typical hardware | CPU or GPU | Primarily GPU servers |
| Several requests | Limited/small-scale concurrency | Continuous batching for many requests |
| Memory management | Simpler runtime management | PagedAttention and efficient KV-cache management |
| Setup | Easier | More setup and GPU/server configuration |
| Model format | GGUF/quantized local builds | Hugging Face-style model weights and supported quantizations |
| One student using my scenario | **Ollama** — simple and local | Not necessary |
| 100 users at once | Not my choice | **vLLM** — designed for shared GPU serving and batching |

For my one-user laptop scenario, Ollama is sufficient. If the same study assistant had to serve around 100 users simultaneously, I would move the serving layer to a GPU server using vLLM or a similar production inference server.

## 11. Hands-on observations

I created `study-assistant` with Ollama and tested it through the REST API.

### Observation table

| Run | Prompt | Modelfile behaviour | TTFT | Total time | Tokens/sec | Warm/cold |
|---|---|---|---:|---:|---:|---|
| 1 | What is a Java class? | Followed study-assistant behaviour | **record from output** | **record** | **record** | First run |
| 2 | Explain what an API is | Followed study-assistant behaviour | **record** | **record** | **record** | Warm run |
| 3 | What is inheritance in Java? | Program system prompt changed style to 3 bullets | N/A/record | **record** | **record** | Warm run |
| 4 | Repeat the API prompt | Same behaviour; compare speed | **record** | **record** | **record** | Warm run |

The important comparison is between the first and repeated run. When the model is already loaded, the second run should avoid the initial model-loading cost. `ollama ps` is used to confirm that `study-assistant` is loaded.

Replace the bold placeholders in this table with the exact values printed by my run before submission.

## 12. Suitability

Ollama is a good fit for my scenario because only one student is using the model, the model is small, and local serving is simple. The Modelfile adds a reusable default personality and rules, while the REST API allows the same model to be used from Python instead of only from the terminal.

A shared deployment for a large number of users would need a serving system designed for concurrency. In that situation, vLLM is more suitable because continuous batching and efficient KV-cache management are designed for high-throughput GPU serving.

## 13. Conclusion

For a local student application, model size, context length, and quantization should be chosen according to available memory and the quality required. A small quantized model is often enough when the task is simple and the machine has limited resources. Context length becomes important when prompts or conversations are long because the KV cache consumes additional memory. A larger model can improve capability but increases memory and serving cost.

For one local user, Ollama provides a simple path from a model to a usable HTTP service. A Modelfile packages default behaviour, and the REST/OpenAI-compatible APIs make programmatic use easier. When many users share the same model, memory fragmentation, KV-cache usage, scheduling, throughput and latency become much more important. That is where a production inference server such as vLLM becomes more appropriate.
