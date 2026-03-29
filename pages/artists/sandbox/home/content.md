<style>
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f5f2ed;
    color: #2a2a28;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    margin: 0;
}
.container {
    text-align: center;
    max-width: 480px;
    padding: 40px;
}
h1 {
    font-size: 48px;
    font-weight: 300;
    margin-bottom: 12px;
}
p {
    color: #6b6860;
    font-size: 14px;
    line-height: 1.7;
}
</style>
<html>
<div class="container">
    <h1>Sandbox</h1>
    <p>This is a blank canvas. Use the Vibe Coder to build something.</p>
</div>

<script>
// Error 1: Undefined variable
try {
    console.log(thisVariableDoesNotExist);
} catch(e) {
    console.error('Error 1:', e);
}

// Error 2: Calling undefined function
try {
    nonExistentFunction();
} catch(e) {
    console.error('Error 2:', e);
}

// Error 3: Type error
try {
    const obj = null;
    obj.someMethod();
} catch(e) {
    console.error('Error 3:', e);
}

// Error 4: Reference error
try {
    let x = undefinedThing + 5;
} catch(e) {
    console.error('Error 4:', e);
}
</script>
</html>
