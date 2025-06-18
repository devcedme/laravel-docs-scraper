# Source: https://laravel.com/docs/12.x/console-tests

# Console Tests

  * Introduction
  * Success / Failure Expectations
  * Input / Output Expectations
  * Console Events



## Introduction

In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/12.x/artisan).

## Success / Failure Expectations

To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code:

Pest PHPUnit

```php test('console command', function () { $this->artisan('inspire')->assertExitCode(0); }); ``` ```php /** * Test a console command. */ public function test_console_command(): void { $this->artisan('inspire')->assertExitCode(0); } ``` 

You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code:

```php $this->artisan('inspire')->assertNotExitCode(1); ``` 

Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not:

```php $this->artisan('inspire')->assertSuccessful(); $this->artisan('inspire')->assertFailed(); ``` 

## Input / Output Expectations

Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command:

```php Artisan::command('question', function () { $name = $this->ask('What is your name?'); $language = $this->choice('Which language do you prefer?', [ 'PHP', 'Ruby', 'Python', ]); $this->line('Your name is '.$name.' and you prefer '.$language.'.'); }); ``` 

You may test this command with the following test:

Pest PHPUnit

```php test('console command', function () { $this->artisan('question') ->expectsQuestion('What is your name?', 'Taylor Otwell') ->expectsQuestion('Which language do you prefer?', 'PHP') ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.') ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.') ->assertExitCode(0); }); ``` ```php /** * Test a console command. */ public function test_console_command(): void { $this->artisan('question') ->expectsQuestion('What is your name?', 'Taylor Otwell') ->expectsQuestion('Which language do you prefer?', 'PHP') ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.') ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.') ->assertExitCode(0); } ``` 

If you are utilizing the `search` or `multisearch` functions provided by [Laravel Prompts](/docs/12.x/prompts), you may use the `expectsSearch` assertion to mock the user's input, search results, and selection:

Pest PHPUnit

```php test('console command', function () { $this->artisan('example') ->expectsSearch('What is your name?', search: 'Tay', answers: [ 'Taylor Otwell', 'Taylor Swift', 'Darian Taylor' ], answer: 'Taylor Otwell') ->assertExitCode(0); }); ``` ```php /** * Test a console command. */ public function test_console_command(): void { $this->artisan('example') ->expectsSearch('What is your name?', search: 'Tay', answers: [ 'Taylor Otwell', 'Taylor Swift', 'Darian Taylor' ], answer: 'Taylor Otwell') ->assertExitCode(0); } ``` 

You may also assert that a console command does not generate any output using the `doesntExpectOutput` method:

Pest PHPUnit

```php test('console command', function () { $this->artisan('example') ->doesntExpectOutput() ->assertExitCode(0); }); ``` ```php /** * Test a console command. */ public function test_console_command(): void { $this->artisan('example') ->doesntExpectOutput() ->assertExitCode(0); } ``` 

The `expectsOutputToContain` and `doesntExpectOutputToContain` methods may be used to make assertions against a portion of the output:

Pest PHPUnit

```php test('console command', function () { $this->artisan('example') ->expectsOutputToContain('Taylor') ->assertExitCode(0); }); ``` ```php /** * Test a console command. */ public function test_console_command(): void { $this->artisan('example') ->expectsOutputToContain('Taylor') ->assertExitCode(0); } ``` 

#### Confirmation Expectations

When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method:

```php $this->artisan('module:import') ->expectsConfirmation('Do you really wish to run this command?', 'no') ->assertExitCode(1); ``` 

#### Table Expectations

If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument:

```php $this->artisan('users:all') ->expectsTable([ 'ID', 'Email', ], [ [1, '[email protected]'], [2, '[email protected]'], ]); ``` 

## Console Events

By default, the `Illuminate\Console\Events\CommandStarting` and `Illuminate\Console\Events\CommandFinished` events are not dispatched while running your application's tests. However, you can enable these events for a given test class by adding the `Illuminate\Foundation\Testing\WithConsoleEvents` trait to the class:

Pest PHPUnit

```php <?php use Illuminate\Foundation\Testing\WithConsoleEvents; uses(WithConsoleEvents::class); // ... ``` ```php <?php namespace Tests\Feature; use Illuminate\Foundation\Testing\WithConsoleEvents; use Tests\TestCase; class ConsoleEventTest extends TestCase { use WithConsoleEvents; // ... } ``` 
