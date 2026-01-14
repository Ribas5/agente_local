# few_shot.py

exemplos = """
Examples of accessibility implementations in Android with Jetpack Compose (Bad vs Good):

**1. Text Contrast:**

- **Bad:**
  - Code:
    ```kotlin
    Text(
        text = "Forgot password",
        color = Color(0xFFAAAAAA), // Light gray on white background
        modifier = Modifier.background(Color.White)
    )
    ```
  - Problem: Contrast is too low, making it difficult for people with low vision to read.

- **Good:**
  - Code:
    ```kotlin
    Text(
        text = "Forgot password",
        color = MaterialTheme.colorScheme.onSurface, // Uses theme color with guaranteed high contrast
        modifier = Modifier.background(MaterialTheme.colorScheme.surface)
    )
    ```
  - Explanation: Use `MaterialTheme` colors or ensure a contrast ratio of at least 4.5:1 for normal text.

**2. Content Descriptions:**

- **Bad:**
  - Code:
    ```kotlin
    Icon(
        imageVector = Icons.Default.Add,
        contentDescription = null, // TalkBack will ignore this button or just say "Button"
        modifier = Modifier.clickable { }
    )
    ```
  - Problem: Interactive elements need a description so the screen reader explains what they do.

- **Good:**
  - Code:
    ```kotlin
    Icon(
        imageVector = Icons.Default.Add,
        contentDescription = "Add new item", // Clear description of the action
        modifier = Modifier.clickable { }
    )
    ```

**3. Touch Target Size:**

- **Bad:**
  - Code:
    ```kotlin
    // Custom button too small (24dp)
    Box(
        modifier = Modifier
            .size(24.dp)
            .background(Color.Blue)
            .clickable { /* Action */ }
    )
    ```
  - Problem: Difficult to click for people with motor impairments or large fingers. The recommended minimum is 48dp.

- **Good:**
  - Code:
    ```kotlin
    // Option A: Use standard components that already have minimum size
    IconButton(onClick = { /* Action */ }) {
        Icon(Icons.Default.Menu, contentDescription = "Menu")
    }

    // Option B: Force minimum size on custom components
    Box(
        modifier = Modifier
            .defaultMinSize(minWidth = 48.dp, minHeight = 48.dp) // Ensures touch area
            .background(Color.Blue)
            .clickable { /* Action */ },
        contentAlignment = Alignment.Center
    ) {
        Text("OK", color = Color.White)
    }
    ```

**4. Text Fields and Labels:**

- **Bad:**
  - Code:
    ```kotlin
    // BasicTextField without semantic label
    var text by remember { mutableStateOf("") }
    BasicTextField(
        value = text,
        onValueChange = { text = it },
        modifier = Modifier.padding(16.dp)
    )
    ```
  - Problem: The user doesn't know what to type, and the screen reader doesn't announce the field's purpose.

- **Good:**
  - Code:
    ```kotlin
    var text by remember { mutableStateOf("") }
    OutlinedTextField(
        value = text,
        onValueChange = { text = it },
        label = { Text("Username") }, // Visible label announced by TalkBack
        modifier = Modifier.fillMaxWidth()
    )
    ```
"""