# Source: https://laravel.com/docs/12.x/responses

# HTTP Responses

  * Creating Responses
    * Attaching Headers to Responses
    * Attaching Cookies to Responses
    * Cookies and Encryption
  * Redirects
    * Redirecting to Named Routes
    * Redirecting to Controller Actions
    * Redirecting to External Domains
    * Redirecting With Flashed Session Data
  * Other Response Types
    * View Responses
    * JSON Responses
    * File Downloads
    * File Responses
  * Streamed Responses
    * Consuming Streamed Responses
    * Streamed JSON Responses
    * Event Streams (SSE)
    * Streamed Downloads
  * Response Macros



## Creating Responses

#### Strings and Arrays

All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response:

```php Route::get('/', function () { return 'Hello World'; }); ``` 

In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response:

```php Route::get('/', function () { return [1, 2, 3]; }); ``` 

Did you know you can also return [Eloquent collections](/docs/12.x/eloquent-collections) from your routes or controllers? They will automatically be converted to JSON. Give it a shot!

#### Response Objects

Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/12.x/views).

Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses:

```php Route::get('/home', function () { return response('Hello World', 200) ->header('Content-Type', 'text/plain'); }); ``` 

#### Eloquent Models and Collections

You may also return [Eloquent ORM](/docs/12.x/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/12.x/eloquent-serialization#hiding-attributes-from-json):

```php use App\Models\User; Route::get('/user/{user}', function (User $user) { return $user; }); ``` 

### Attaching Headers to Responses

Keep in mind that most response methods are chainable, allowing for the fluent construction of response instances. For example, you may use the `header` method to add a series of headers to the response before sending it back to the user:

```php return response($content) ->header('Content-Type', $type) ->header('X-Header-One', 'Header Value') ->header('X-Header-Two', 'Header Value'); ``` 

Or, you may use the `withHeaders` method to specify an array of headers to be added to the response:

```php return response($content) ->withHeaders([ 'Content-Type' => $type, 'X-Header-One' => 'Header Value', 'X-Header-Two' => 'Header Value', ]); ``` 

#### Cache Control Middleware

Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier:

```php Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () { Route::get('/privacy', function () { // ... }); Route::get('/terms', function () { // ... }); }); ``` 

### Attaching Cookies to Responses

You may attach a cookie to an outgoing `Illuminate\Http\Response` instance using the `cookie` method. You should pass the name, value, and the number of minutes the cookie should be considered valid to this method:

```php return response('Hello World')->cookie( 'name', 'value', $minutes ); ``` 

The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method:

```php return response('Hello World')->cookie( 'name', 'value', $minutes, $path, $domain, $secure, $httpOnly ); ``` 

If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser:

```php use Illuminate\Support\Facades\Cookie; Cookie::queue('name', 'value', $minutes); ``` 

#### Generating Cookie Instances

If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance:

```php $cookie = cookie('name', 'value', $minutes); return response('Hello World')->cookie($cookie); ``` 

#### Expiring Cookies Early

You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response:

```php return response('Hello World')->withoutCookie('name'); ``` 

If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie:

```php Cookie::expire('name'); ``` 

### Cookies and Encryption

By default, thanks to the `Illuminate\Cookie\Middleware\EncryptCookies` middleware, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `encryptCookies` method in your application's `bootstrap/app.php` file:

```php ->withMiddleware(function (Middleware $middleware) { $middleware->encryptCookies(except: [ 'cookie_name', ]); }) ``` 

## Redirects

Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper:

```php Route::get('/dashboard', function () { return redirect('/home/dashboard'); }); ``` 

Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/12.x/session), make sure the route calling the `back` function is using the `web` middleware group:

```php Route::post('/user/profile', function () { // Validate the request... return back()->withInput(); }); ``` 

### Redirecting to Named Routes

When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method:

```php return redirect()->route('login'); ``` 

If your route has parameters, you may pass them as the second argument to the `route` method:

```php // For a route with the following URI: /profile/{id} return redirect()->route('profile', ['id' => 1]); ``` 

#### Populating Parameters via Eloquent Models

If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically:

```php // For a route with the following URI: /profile/{id} return redirect()->route('profile', [$user]); ``` 

If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model:

```php /** * Get the value of the model's route key. */ public function getRouteKey(): mixed { return $this->slug; } ``` 

### Redirecting to Controller Actions

You may also generate redirects to [controller actions](/docs/12.x/controllers). To do so, pass the controller and action name to the `action` method:

```php use App\Http\Controllers\UserController; return redirect()->action([UserController::class, 'index']); ``` 

If your controller route requires parameters, you may pass them as the second argument to the `action` method:

```php return redirect()->action( [UserController::class, 'profile'], ['id' => 1] ); ``` 

### Redirecting to External Domains

Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification:

```php return redirect()->away('https://www.google.com'); ``` 

### Redirecting With Flashed Session Data

Redirecting to a new URL and [flashing data to the session](/docs/12.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain:

```php Route::post('/user/profile', function () { // ... return redirect('/dashboard')->with('status', 'Profile updated!'); }); ``` 

After the user is redirected, you may display the flashed message from the [session](/docs/12.x/session). For example, using [Blade syntax](/docs/12.x/blade):

```blade @if (session('status')) <div class="alert alert-success"> {{ session('status') }} </div> @endif ``` 

#### Redirecting With Input

You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/12.x/requests#retrieving-old-input) during the next request to repopulate the form:

```php return back()->withInput(); ``` 

## Other Response Types

The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/12.x/contracts) is returned. This contract provides several helpful methods for generating responses.

### View Responses

If you need control over the response's status and headers but also need to return a [view](/docs/12.x/views) as the response's content, you should use the `view` method:

```php return response() ->view('hello', $data, 200) ->header('Content-Type', $type); ``` 

Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function.

### JSON Responses

The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function:

```php return response()->json([ 'name' => 'Abigail', 'state' => 'CA', ]); ``` 

If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method:

```php return response() ->json(['name' => 'Abigail', 'state' => 'CA']) ->withCallback($request->input('callback')); ``` 

### File Downloads

The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method:

```php return response()->download($pathToFile); return response()->download($pathToFile, $name, $headers); ``` 

Symfony HttpFoundation, which manages file downloads, requires the file being downloaded to have an ASCII filename.

### File Responses

The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the absolute path to the file as its first argument and an array of headers as its second argument:

```php return response()->file($pathToFile); return response()->file($pathToFile, $headers); ``` 

## Streamed Responses

By streaming data to the client as it is generated, you can significantly reduce memory usage and improve performance, especially for very large responses. Streamed responses allow the client to begin processing data before the server has finished sending it:

```php Route::get('/stream', function () { return response()->stream(function (): void { foreach (['developer', 'admin'] as $string) { echo $string; ob_flush(); flush(); sleep(2); // Simulate delay between chunks... } }, 200, ['X-Accel-Buffering' => 'no']); }); ``` 

For convenience, if the closure you provide to the `stream` method returns a [Generator](https://www.php.net/manual/en/language.generators.overview.php), Laravel will automatically flush the output buffer between strings returned by the generator, as well as disable Nginx output buffering:

```php Route::post('/chat', function () { return response()->stream(function (): void { $stream = OpenAI::client()->chat()->createStreamed(...); foreach ($stream as $response) { yield $response->choices[0]; } }); }); ``` 

### Consuming Streamed Responses

Streamed responses may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel response and event streams. To get started, install the `@laravel/stream-react` or `@laravel/stream-vue` package:

React Vue

```shell npm install @laravel/stream-react ``` ```shell npm install @laravel/stream-vue ``` 

Then, `useStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `data` with the concatenated response as content is returned from your Laravel application:

React Vue

```tsx import { useStream } from "@laravel/stream-react"; function App() { const { data, isFetching, isStreaming, send } = useStream("chat"); const sendMessage = () => { send({ message: `Current timestamp: ${Date.now()}`, }); }; return ( <div> <div>{data}</div> {isFetching && <div>Connecting...</div>} {isStreaming && <div>Generating...</div>} <button onClick={sendMessage}>Send Message</button> </div> ); } ``` ```vue <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; const { data, isFetching, isStreaming, send } = useStream("chat"); const sendMessage = () => { send({ message: `Current timestamp: ${Date.now()}`, }); }; </script> <template> <div> <div>{{ data }}</div> <div v-if="isFetching">Connecting...</div> <div v-if="isStreaming">Generating...</div> <button @click="sendMessage">Send Message</button> </div> </template> ``` 

When sending data back to the stream via `send`, the active connection to the stream is canceled before sending the new data. All requests are sent as JSON `POST` requests.

Since the `useStream` hook makes a `POST` request to your application, a valid CSRF token is required. The easiest way to provide the CSRF token is to [include it via a `meta` tag in your application layout's `head`](/docs/12.x/csrf#csrf-x-csrf-token).

The second argument given to `useStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below:

React Vue

```tsx import { useStream } from "@laravel/stream-react"; function App() { const { data } = useStream("chat", { id: undefined, initialInput: undefined, headers: undefined, csrfToken: undefined, onResponse: (response: Response) => void, onData: (data: string) => void, onCancel: () => void, onFinish: () => void, onError: (error: Error) => void, }); return <div>{data}</div>; } ``` ```vue <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; const { data } = useStream("chat", { id: undefined, initialInput: undefined, headers: undefined, csrfToken: undefined, onResponse: (response: Response) => void, onData: (data: string) => void, onCancel: () => void, onFinish: () => void, onError: (error: Error) => void, }); </script> <template> <div>{{ data }}</div> </template> ``` 

`onResponse` is triggered after a successful initial response from the stream and the raw [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) is passed to the callback. `onData` is called as each chunk is received - the current chunk is passed to the callback. `onFinish` is called when a stream has finished and when an error is thrown during the fetch / read cycle.

By default, a request is not made to the stream on initialization. You may pass an initial payload to the stream by using the `initialInput` option:

React Vue

```tsx import { useStream } from "@laravel/stream-react"; function App() { const { data } = useStream("chat", { initialInput: { message: "Introduce yourself.", }, }); return <div>{data}</div>; } ``` ```vue <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; const { data } = useStream("chat", { initialInput: { message: "Introduce yourself.", }, }); </script> <template> <div>{{ data }}</div> </template> ``` 

To cancel a stream manually, you may use the `cancel` method returned from the hook:

React Vue

```tsx import { useStream } from "@laravel/stream-react"; function App() { const { data, cancel } = useStream("chat"); return ( <div> <div>{data}</div> <button onClick={cancel}>Cancel</button> </div> ); } ``` ```vue <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; const { data, cancel } = useStream("chat"); </script> <template> <div> <div>{{ data }}</div> <button @click="cancel">Cancel</button> </div> </template> ``` 

Each time the `useStream` hook is used, a random `id` is generated to identify the stream. This is sent back to the server with each request in the `X-STREAM-ID` header. When consuming the same stream from multiple components, you can read and write to the stream by providing your own `id`:

React Vue

```tsx // App.tsx import { useStream } from "@laravel/stream-react"; function App() { const { data, id } = useStream("chat"); return ( <div> <div>{data}</div> <StreamStatus id={id} /> </div> ); } // StreamStatus.tsx import { useStream } from "@laravel/stream-react"; function StreamStatus({ id }) { const { isFetching, isStreaming } = useStream("chat", { id }); return ( <div> {isFetching && <div>Connecting...</div>} {isStreaming && <div>Generating...</div>} </div> ); } ``` ```vue <!-- App.vue --> <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; import StreamStatus from "./StreamStatus.vue"; const { data, id } = useStream("chat"); </script> <template> <div> <div>{{ data }}</div> <StreamStatus :id="id" /> </div> </template> <!-- StreamStatus.vue --> <script setup lang="ts"> import { useStream } from "@laravel/stream-vue"; const props = defineProps<{ id: string; }>(); const { isFetching, isStreaming } = useStream("chat", { id: props.id }); </script> <template> <div> <div v-if="isFetching">Connecting...</div> <div v-if="isStreaming">Generating...</div> </div> </template> ``` 

### Streamed JSON Responses

If you need to stream JSON data incrementally, you may utilize the `streamJson` method. This method is especially useful for large datasets that need to be sent progressively to the browser in a format that can be easily parsed by JavaScript:

```php use App\Models\User; Route::get('/users.json', function () { return response()->streamJson([ 'users' => User::cursor(), ]); }); ``` 

The `useJsonStream` hook is identical to the `useStream` hook except that it will attempt to parse the data as JSON once it has finished streaming:

React Vue

```tsx import { useJsonStream } from "@laravel/stream-react"; type User = { id: number; name: string; email: string; }; function App() { const { data, send } = useJsonStream<{ users: User[] }>("users"); const loadUsers = () => { send({ query: "taylor", }); }; return ( <div> <ul> {data?.users.map((user) => ( <li> {user.id}: {user.name} </li> ))} </ul> <button onClick={loadUsers}>Load Users</button> </div> ); } ``` ```vue <script setup lang="ts"> import { useJsonStream } from "@laravel/stream-vue"; type User = { id: number; name: string; email: string; }; const { data, send } = useJsonStream<{ users: User[] }>("users"); const loadUsers = () => { send({ query: "taylor", }); }; </script> <template> <div> <ul> <li v-for="user in data?.users" :key="user.id"> {{ user.id }}: {{ user.name }} </li> </ul> <button @click="loadUsers">Load Users</button> </div> </template> ``` 

### Event Streams (SSE)

The `eventStream` method may be used to return a server-sent events (SSE) streamed response using the `text/event-stream` content type. The `eventStream` method accepts a closure which should [yield](https://www.php.net/manual/en/language.generators.overview.php) responses to the stream as the responses become available:

```php Route::get('/chat', function () { return response()->eventStream(function () { $stream = OpenAI::client()->chat()->createStreamed(...); foreach ($stream as $response) { yield $response->choices[0]; } }); }); ``` 

If you would like to customize the name of the event, you may yield an instance of the `StreamedEvent` class:

```php use Illuminate\Http\StreamedEvent; yield new StreamedEvent( event: 'update', data: $response->choices[0], ); ``` 

#### Consuming Event Streams

Event streams may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel event streams. To get started, install the `@laravel/stream-react` or `@laravel/stream-vue` package:

React Vue

```shell npm install @laravel/stream-react ``` ```shell npm install @laravel/stream-vue ``` 

Then, `useEventStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `message` with the concatenated response as messages are returned from your Laravel application:

React Vue

```jsx import { useEventStream } from "@laravel/stream-react"; function App() { const { message } = useEventStream("/chat"); return <div>{message}</div>; } ``` ```vue <script setup lang="ts"> import { useEventStream } from "@laravel/stream-vue"; const { message } = useEventStream("/chat"); </script> <template> <div>{{ message }}</div> </template> ``` 

The second argument given to `useEventStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below:

React Vue

```jsx import { useEventStream } from "@laravel/stream-react"; function App() { const { message } = useEventStream("/stream", { event: "update", onMessage: (message) => { // }, onError: (error) => { // }, onComplete: () => { // }, endSignal: "</stream>", glue: " ", }); return <div>{message}</div>; } ``` ```vue <script setup lang="ts"> import { useEventStream } from "@laravel/stream-vue"; const { message } = useEventStream("/chat", { event: "update", onMessage: (message) => { // ... }, onError: (error) => { // ... }, onComplete: () => { // ... }, endSignal: "</stream>", glue: " ", }); </script> ``` 

Event streams may also be manually consumed via an [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) object by your application's frontend. The `eventStream` method will automatically send a `</stream>` update to the event stream when the stream is complete:

```js const source = new EventSource('/chat'); source.addEventListener('update', (event) => { if (event.data === '</stream>') { source.close(); return; } console.log(event.data); }); ``` 

To customize the final event that is sent to the event stream, you may provide a `StreamedEvent` instance to the `eventStream` method's `endStreamWith` argument:

```php return response()->eventStream(function () { // ... }, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>')); ``` 

### Streamed Downloads

Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments:

```php use App\Services\GitHub; return response()->streamDownload(function () { echo GitHub::api('repo') ->contents() ->readme('laravel', 'laravel')['contents']; }, 'laravel-readme.md'); ``` 

## Response Macros

If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/12.x/providers), such as the `App\Providers\AppServiceProvider` service provider:

```php <?php namespace App\Providers; use Illuminate\Support\Facades\Response; use Illuminate\Support\ServiceProvider; class AppServiceProvider extends ServiceProvider { /** * Bootstrap any application services. */ public function boot(): void { Response::macro('caps', function (string $value) { return Response::make(strtoupper($value)); }); } } ``` 

The `macro` function accepts a name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper:

```php return response()->caps('foo'); ``` 
