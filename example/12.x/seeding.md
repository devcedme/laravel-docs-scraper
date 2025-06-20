# Source: https://laravel.com/docs/12.x/seeding

# Database: Seeding

  * Introduction
  * Writing Seeders
    * Using Model Factories
    * Calling Additional Seeders
    * Muting Model Events
  * Running Seeders



## Introduction

Laravel includes the ability to seed your database with data using seed classes. All seed classes are stored in the `database/seeders` directory. By default, a `DatabaseSeeder` class is defined for you. From this class, you may use the `call` method to run other seed classes, allowing you to control the seeding order.

[Mass assignment protection](/docs/12.x/eloquent#mass-assignment) is automatically disabled during database seeding.

## Writing Seeders

To generate a seeder, execute the `make:seeder` [Artisan command](/docs/12.x/artisan). All seeders generated by the framework will be placed in the `database/seeders` directory:

```shell php artisan make:seeder UserSeeder ``` 

A seeder class only contains one method by default: `run`. This method is called when the `db:seed` [Artisan command](/docs/12.x/artisan) is executed. Within the `run` method, you may insert data into your database however you wish. You may use the [query builder](/docs/12.x/queries) to manually insert data or you may use [Eloquent model factories](/docs/12.x/eloquent-factories).

As an example, let's modify the default `DatabaseSeeder` class and add a database insert statement to the `run` method:

```php <?php namespace Database\Seeders; use Illuminate\Database\Seeder; use Illuminate\Support\Facades\DB; use Illuminate\Support\Facades\Hash; use Illuminate\Support\Str; class DatabaseSeeder extends Seeder { /** * Run the database seeders. */ public function run(): void { DB::table('users')->insert([ 'name' => Str::random(10), 'email' => Str::random(10).'@example.com', 'password' => Hash::make('password'), ]); } } ``` 

You may type-hint any dependencies you need within the `run` method's signature. They will automatically be resolved via the Laravel [service container](/docs/12.x/container).

### Using Model Factories

Of course, manually specifying the attributes for each model seed is cumbersome. Instead, you can use [model factories](/docs/12.x/eloquent-factories) to conveniently generate large amounts of database records. First, review the [model factory documentation](/docs/12.x/eloquent-factories) to learn how to define your factories.

For example, let's create 50 users that each has one related post:

```php use App\Models\User; /** * Run the database seeders. */ public function run(): void { User::factory() ->count(50) ->hasPosts(1) ->create(); } ``` 

### Calling Additional Seeders

Within the `DatabaseSeeder` class, you may use the `call` method to execute additional seed classes. Using the `call` method allows you to break up your database seeding into multiple files so that no single seeder class becomes too large. The `call` method accepts an array of seeder classes that should be executed:

```php /** * Run the database seeders. */ public function run(): void { $this->call([ UserSeeder::class, PostSeeder::class, CommentSeeder::class, ]); } ``` 

### Muting Model Events

While running seeds, you may want to prevent models from dispatching events. You may achieve this using the `WithoutModelEvents` trait. When used, the `WithoutModelEvents` trait ensures no model events are dispatched, even if additional seed classes are executed via the `call` method:

```php <?php namespace Database\Seeders; use Illuminate\Database\Seeder; use Illuminate\Database\Console\Seeds\WithoutModelEvents; class DatabaseSeeder extends Seeder { use WithoutModelEvents; /** * Run the database seeders. */ public function run(): void { $this->call([ UserSeeder::class, ]); } } ``` 

## Running Seeders

You may execute the `db:seed` Artisan command to seed your database. By default, the `db:seed` command runs the `Database\Seeders\DatabaseSeeder` class, which may in turn invoke other seed classes. However, you may use the `--class` option to specify a specific seeder class to run individually:

```shell php artisan db:seed php artisan db:seed --class=UserSeeder ``` 

You may also seed your database using the `migrate:fresh` command in combination with the `--seed` option, which will drop all tables and re-run all of your migrations. This command is useful for completely re-building your database. The `--seeder` option may be used to specify a specific seeder to run:

```shell php artisan migrate:fresh --seed php artisan migrate:fresh --seed --seeder=UserSeeder ``` 

#### Forcing Seeders to Run in Production

Some seeding operations may cause you to alter or lose data. In order to protect you from running seeding commands against your production database, you will be prompted for confirmation before the seeders are executed in the `production` environment. To force the seeders to run without a prompt, use the `--force` flag:

```shell php artisan db:seed --force ``` 
