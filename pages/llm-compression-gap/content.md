<style>
/* Personal narrative blog styling */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    line-height: 1.7;
    color: #2c3e50;
    background: #fdfdfd;
    margin: 0;
    padding: 24px;
    font-size: 17px;
    max-width: 800px;
    margin: 0 auto;
}

.container {
    background: white;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    overflow: hidden;
}

.header {
    background: linear-gradient(135deg, #003366 0%, #0066cc 100%);
    color: white;
    padding: 40px;
    text-align: center;
}

.content {
    padding: 40px;
}

/* Typography */
h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 15px 0;
    line-height: 1.2;
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    font-weight: 400;
    margin: 0 0 20px 0;
    line-height: 1.4;
}

.meta {
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 14px;
    display: inline-block;
}

h2 {
    font-size: 1.6rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 45px 0 25px 0;
    border-bottom: 2px solid #f1f3f4;
    padding-bottom: 12px;
}

h3 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #34495e;
    margin: 35px 0 18px 0;
}

p {
    margin-bottom: 22px;
    color: #2c3e50;
    text-align: left;
}

/* Story elements */
.story-moment {
    background: #fffbf0;
    border: 2px solid #ffd700;
    padding: 25px;
    margin: 30px 0;
    border-radius: 6px;
    position: relative;
}

.realization {
    background: #f0f8ff;
    border: 2px solid #0066cc;
    padding: 25px;
    margin: 30px 0;
    border-radius: 6px;
}

.realization h3 {
    color: #003366;
    margin-top: 0;
    margin-bottom: 15px;
}

/* Tables */
.comparison-table {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    padding: 25px;
    margin: 30px 0;
    border-radius: 6px;
    overflow-x: auto;
}

.comparison-table h4 {
    color: #495057;
    margin: 0 0 20px 0;
    text-align: center;
    font-size: 1.1rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    background: white;
    border-radius: 4px;
    overflow: hidden;
}

th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
}

th {
    background: #343a40;
    color: white;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.winner-row {
    background: #d4edda;
    font-weight: 600;
}

.llm-row {
    background: #fff3cd;
    font-weight: 500;
}

/* Quote box */
.reddit-quote {
    background: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 25px;
    margin: 30px 0;
    font-style: italic;
    position: relative;
}

.reddit-quote::before {
    content: '"';
    font-size: 4rem;
    color: #57606a;
    position: absolute;
    top: 10px;
    left: 15px;
    line-height: 1;
}

.reddit-quote-content {
    margin-left: 30px;
}

.reddit-quote-attribution {
    text-align: right;
    font-style: normal;
    font-weight: 600;
    color: #656d76;
    margin-top: 15px;
    font-size: 14px;
}

/* Insights */
.insight {
    background: #fff9e6;
    border: 2px solid #ffcc00;
    padding: 25px;
    margin: 30px 0;
    border-radius: 6px;
}

.insight h3 {
    color: #cc8800;
    margin-top: 0;
    margin-bottom: 15px;
}

/* Links */
a {
    color: #0066cc;
    text-decoration: none;
    font-weight: 500;
}

a:hover {
    text-decoration: underline;
}

/* Code */
code {
    background: #f1f3f4;
    color: #d73a49;
    padding: 3px 6px;
    border-radius: 3px;
    font-family: 'SF Mono', Consolas, monospace;
    font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
    body {
        padding: 12px;
        font-size: 16px;
    }
    
    .container {
        border: none;
        border-radius: 0;
        box-shadow: none;
    }
    
    .content, .header {
        padding: 24px 20px;
    }
    
    h1 {
        font-size: 1.8rem;
    }
    
    h2 {
        font-size: 1.4rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
    }
    
    .comparison-table {
        padding: 15px;
        margin: 20px 0;
    }
    
    table {
        font-size: 12px;
        min-width: 500px;
    }
    
    th, td {
        padding: 8px 10px;
    }
    
    .reddit-quote {
        padding: 20px 15px;
    }
    
    .reddit-quote-content {
        margin-left: 25px;
    }
}
</style>

<html>
<div class="container">
    <div class="header">
        <h1>The LLM Compression Gap</h1>
        <div class="subtitle">Exploring the gap between LLM compression performance and competition constraints</div>
        <div class="meta">Published August 20, 2025 | Research Analysis</div>
    </div>

    <div class="content">
        <p>The relationship between compression and intelligence has fascinated researchers for decades. The Hutter Prize embodies this connection, offering €500,000 for better Wikipedia compression. But there's a fundamental gap between what works in theory and what the prize constraints allow.</p>

        <div class="story-moment">
            <p><strong><a href="http://prize.hutter1.net/" target="_blank">Visit the Hutter Prize website</a></strong></p>
            I first encountered the Hutter Prize while researching compression algorithms. €500,000 for compressing Wikipedia better than anyone else had managed. The premise was elegant: compression equals prediction equals intelligence. If you can compress data better, you understand it better.
        </div>

        <p>If modern language models are getting eerily good at predicting what comes next in text, and compression is fundamentally about prediction, shouldn't LLMs be absolutely crushing traditional compression algorithms? During a long moped ride through northern Vietnam, I found myself thinking about this connection more seriously.</p>

        <h2>A Simple Idea</h2>

        <p>The idea seemed straightforward: instead of storing actual words, what if you stored their likelihood according to an LLM? If the model predicts "dangerous" is the 3rd most likely next word, just store "3" instead of "dangerous."</p>

        <div class="realization">
            <h3>The Core Idea</h3>
            <p>High-probability words get low ranks (0, 1, 2) which compress extremely well. Unexpected words get high ranks, but that's okay because they're rare. The better your language model understands the text, the more often it predicts correctly, yielding better compression.</p>
        </div>

        <p>As most good daydream ideas go, if it seems obvious, someone has probably tried it. I was glad to discover there was indeed research in this direction.</p>

        <h2>LLMZip: The Idea in Practice</h2>

        <p>A quick search revealed <a href="https://arxiv.org/abs/2306.04050">LLMZip</a> and <a href="https://arxiv.org/html/2409.17141v1">FineZip</a> - papers that had implemented exactly this approach. The results were impressive.</p>

        <div class="comparison-table">
            <h4>Compression Performance Comparison</h4>
            <table>
                <tr>
                    <th>Method</th>
                    <th>Bits/Character</th>
                    <th>Compression Time</th>
                    <th>Dataset</th>
                    <th>Year</th>
                </tr>
                <tr class="llm-row">
                    <td>LLMZip (LLaMA-7B + AC)</td>
                    <td>0.636</td>
                    <td>~227 hours (10MB)</td>
                    <td>enwik8</td>
                    <td>2023</td>
                </tr>
                <tr class="llm-row">
                    <td>FineZip</td>
                    <td>~0.64</td>
                    <td>~4 hours (10MB)</td>
                    <td>enwik8</td>
                    <td>2024</td>
                </tr>
                <tr>
                    <td>ts_zip (Bellard)</td>
                    <td>1.084</td>
                    <td>~minutes</td>
                    <td>enwik9</td>
                    <td>2023</td>
                </tr>
                <tr class="winner-row">
                    <td>fx2-cmix (Hutter Prize)</td>
                    <td>0.944</td>
                    <td>~50 hours</td>
                    <td>enwik9 (1GB)</td>
                    <td>2024</td>
                </tr>
                <tr>
                    <td>Traditional (zlib)</td>
                    <td>~2.8</td>
                    <td>seconds</td>
                    <td>various</td>
                    <td>-</td>
                </tr>
            </table>
        </div>

        <p>The LLM methods weren't just better - they were dramatically better. LLMZip achieved 0.636 bits per character, compared to the current Hutter Prize winner at 0.944. That's approaching <a href="https://mattmahoney.net/dc/entropy1.html">Shannon's theoretical limit for English text entropy</a> (~0.6-1.3 bpc).</p>

        <h2>The Constraint Problem</h2>

        <p>Then I read the Hutter Prize rules more carefully. The constraints were extremely restrictive.</p>

        <div class="comparison-table">
            <h4>Hutter Prize Constraints vs LLM Requirements</h4>
            <table>
                <tr>
                    <th>Resource</th>
                    <th>Hutter Prize Limit</th>
                    <th>FineZip Needs</th>
                    <th>Gap</th>
                </tr>
                <tr>
                    <td>Time</td>
                    <td>70,000/T hours*</td>
                    <td>~4 hours (10MB)</td>
                    <td>Still 80x too slow</td>
                </tr>
                <tr>
                    <td>Memory</td>
                    <td>10GB RAM</td>
                    <td>~13GB+ (LLaMA-7B)</td>
                    <td>Won't fit</td>
                </tr>
                <tr>
                    <td>GPU Usage</td>
                    <td>Not allowed</td>
                    <td>Essential for speed</td>
                    <td>Impossible</td>
                </tr>
                <tr>
                    <td>Dataset Size</td>
                    <td>1GB (enwik9)</td>
                    <td>Works, but limited</td>
                    <td>Scale mismatch</td>
                </tr>
            </table>
        </div>

        <p style="font-size: 13px; color: #666;">*T = Geekbench5 score. Test machines: Intel i7-1165G7 (T≈1427) = ~49 hours, AMD Ryzen 7 3.6GHz (T≈1310) = ~53 hours</p>

        <p>The math was still brutal. Even with FineZip's 54x speedup over LLMZip, it needed 4 hours just for 10MB. For the full 1GB enwik9 dataset, you'd need roughly 400 hours - about 8 times the Hutter Prize limit, a significant improvement but still prohibitive.</p>

        <h2>Community Perspective</h2>

        <p>Digging deeper, I found a <a href="https://www.reddit.com/r/MachineLearning/comments/jukxk4/d_any_thoughts_on_600k_hutter_prize_for_lossless/">prescient Reddit discussion</a> from 2020 that perfectly captured the problem:</p>

        <div class="reddit-quote">
            <div class="reddit-quote-content">
                The prize has been largely useless because the resource constraints are many orders of magnitude too severe, and the dataset too tiny.<br><br>

                The overall thesis that prediction=intelligence has been very strongly vindicated by, most notably recently in scaled-up language models trained solely with a self-supervised prediction loss who have near-perfect correlation of their perplexity/BPC compression performance with human-like text generation and benchmarks... but not a single SOTA of interest can be trained or run within the original Hutter Prize constraints.<br><br>

                Genuine intelligence requires far more resources and data to amortize itself over than the HP provides. The only things that run within those constraints are things like PAQ8, which are too slow to be of any ordinary software engineering interest... and yet, too cheap to be anything but completely useless to AI/ML research.
            </div>
            <div class="reddit-quote-attribution">
                — <a href="https://www.reddit.com/r/MachineLearning/comments/jukxk4/d_any_thoughts_on_600k_hutter_prize_for_lossless/">r/MachineLearning discussion</a>
            </div>
        </div>

        <p>This crystallized the fundamental tension: the Hutter Prize validates compression=intelligence in theory, but constrains it so severely that actual intelligent systems can't participate.</p>

        <h2>Potential Path Forward</h2>

        <p>There might be one viable path forward. The current Hutter Prize winner fx2-cmix includes sophisticated preprocessing with natural language processing features like stemming and neural network components including LSTM-based context mixing. However, the extent to which modern LLM embeddings are currently used requires further investigation.</p>

        <div class="insight">
            <h3>The Preprocessing Opportunity</h3>
            <p>What if tiny, specialized language models (10-100M parameters) could enhance the semantic understanding in the preprocessing stage? Recent research on neural scaling laws shows these models can retain ~95% of performance through knowledge distillation while fitting easily within memory constraints.</p>
        </div>

        <p>Current compression algorithms like fx2-cmix already incorporate neural networks and semantic processing within the strict computational limits, but there may still be opportunities to improve upon their existing approaches with more targeted models.</p>

        <h2>Scaling Laws and Future Directions</h2>

        <p>Understanding how model performance scales with size is crucial here. Research on <a href="https://www.youtube.com/watch?v=5eqRuVp65eY">neural scaling laws</a> suggests that even tiny models can capture substantial semantic understanding when trained properly.</p>

        <p>The key insight: you don't need GPT-4 scale to get useful semantic compression gains. A 50M parameter model specialized for Wikipedia compression might provide enough semantic boost to edge out the current winner, while still fitting within the absurd constraints.</p>

        <h2>Next Steps: Getting Closer to the Machine</h2>

        <p>I'm planning to dive deeper into how current compression algorithms actually work. After recently working with cloud-based AI systems churning out endless content, there's something appealing about working within real constraints for once. The Hutter Prize forces you to think carefully about every bit, every cycle, every byte of memory.</p>

        <p>My plan is to first understand fx2-cmix's implementation - how exactly does its neural network preprocessing work? What semantic features is it already capturing? Then I'll explore whether there are opportunities to integrate small, specialized models within those brutal constraints.</p>

        <div class="realization">
            <h3>A Different Kind of Challenge</h3>
            <p>Instead of throwing computational resources at problems, this requires genuine optimization and understanding. It's a refreshing change from the "just add more GPUs" approach that dominates modern AI.</p>
        </div>

        <p>The Hutter Prize constraints may be anachronistic, but they create an interesting sandbox for exploring the boundaries between statistical optimization and semantic understanding. Plus, there's something satisfying about trying to squeeze every bit of performance from a system that has to fit in 10GB of RAM.</p>

        <p>I have a lot of respect for Marcus Hutter's rationale behind keeping these constraints so restrictive. As he explains on the website:</p>

        <div class="reddit-quote">
            <div class="reddit-quote-content">
                What if I can (significantly) beat the current record?<br><br>
                
                In this case, submit your code and win the award and/or copyright your code and/or patent your ideas. Also note that a provisional patent application is quite cheap. Thereafter you can enter the competition and fund the expensive non-provisional patent application with the prize money. You should be able to monetize your invention beyond the HKCP. This happened to the first winner, a Russian/Ukrainian who always had to cycle 8km to a friend to test his code because he did not even have a suitable computer, and who now has a lucrative job at QTR in Canada... The mp3 patent (the most famous lossy compressor for music) for instance, made millions of dollars from licensing fees. If your compressor is revolutionary, say beats current SOTA by over 30%, this is most likely due to a mistake or misunderstanding or violation of the rules.
            </div>
            <div class="reddit-quote-attribution">
                — <a href="http://prize.hutter1.net/">Hutter Prize FAQ</a>
            </div>
        </div>

        <p>It's a strange approach to encouraging AI development, but there's wisdom in it. The constraints force genuine innovation rather than just throwing more compute at the problem.</p>

        <p>In my degree right now, all the AI we're covering is old school - we haven't been doing any work with neural networks or transformers. It's all pre-LLM stuff. With the way I'm wired, I find it hard not to take the shortest path to the goal, so there's a certain romanticism I find in wondering what things would be like if the constraints were harder.</p>

        <p>I'll be wielding my army of AI agents to help build frameworks to understand this problem, create the environments and GUIs to assist me like I do with everything now. But hopefully it'll hit a deadlock pretty quickly, and I'll be forced to learn something before I become totally dependent on AI.</p>
    </div>
</div>
</html>