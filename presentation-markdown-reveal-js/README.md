# markdown to presentation with reveal.js
## installation 
```sh
mkdir reveal-js
cd reveal-js
wget https://github.com/hakimel/reveal.js/archive/master.zip
unzip master.zip 
cd reveal.js-master

http-server .
x-www-browser http://localhost:8080
```


## edit index.html
```html
		<div class="reveal">
			<div class="slides">
				<section>Slide 1</section>
				<section>
					<section>
						<h2>Vertical Slides</h2>
						<p>Slides can be nested inside of each other.</p>
						<p>Use the <em>Space</em> key to navigate through all slides.</p>
						<br>
						<a href="#/2/1" class="navigate-down">
							<img class="r-frame" style="background: rgba(255,255,255,0.1);" width="178" height="238" data-src="https://static.slid.es/reveal/arrow.png" alt="Down arrow">
						</a>
					</section>
                    <section data-markdown>
                        ## Markdown Support
                        Write content using inline or external Markdown.
                        [go back](http://localhost:8080/#/2).
                    </section>
                    <section data-markdown>
                        ## Markdown 
                        Write 
                        Instructions
                    </section>

				</section>
			</div>
		</div>

```
