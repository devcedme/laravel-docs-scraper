# Source: https://laravel.com/docs/12.x/migrations

# Database: Migrations

  * Introduction
  * Generating Migrations
    * Squashing Migrations
  * Migration Structure
  * Running Migrations
    * Rolling Back Migrations
  * Tables
    * Creating Tables
    * Updating Tables
    * Renaming / Dropping Tables
  * Columns
    * Creating Columns
    * Available Column Types
    * Column Modifiers
    * Modifying Columns
    * Renaming Columns
    * Dropping Columns
  * Indexes
    * Creating Indexes
    * Renaming Indexes
    * Dropping Indexes
    * Foreign Key Constraints
  * Events



## Introduction

Migrations are like version control for your database, allowing your team to define and share the application's database schema definition. If you have ever had to tell a teammate to manually add a column to their local database schema after pulling in your changes from source control, you've faced the problem that database migrations solve.

The Laravel `Schema` [facade](/docs/12.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns.

## Generating Migrations

You may use the `make:migration` [Artisan command](/docs/12.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations:

```shell php artisan make:migration create_flights_table ``` 

Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually.

If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path.

Migration stubs may be customized using [stub publishing](/docs/12.x/artisan#stub-customization).

### Squashing Migrations

As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command:

```shell php artisan schema:dump # Dump the current database schema and prune all existing migrations... php artisan schema:dump --prune ``` 

When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will first execute the SQL statements in the schema file of the database connection you are using. After executing the schema file's SQL statements, Laravel will execute any remaining migrations that were not part of the schema dump.

If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development:

```shell php artisan schema:dump php artisan schema:dump --database=testing --prune ``` 

You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure.

Migration squashing is only available for the MariaDB, MySQL, PostgreSQL, and SQLite databases and utilizes the database's command-line client.

## Migration Structure

A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method.

Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, check out its documentation. For example, the following migration creates a `flights` table:

```php <?php use Illuminate\Database\Migrations\Migration; use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; return new class extends Migration { /** * Run the migrations. */ public function up(): void { Schema::create('flights', function (Blueprint $table) { $table->id(); $table->string('name'); $table->string('airline'); $table->timestamps(); }); } /** * Reverse the migrations. */ public function down(): void { Schema::drop('flights'); } }; ``` 

#### Setting the Migration Connection

If your migration will be interacting with a database connection other than your application's default database connection, you should set the `$connection` property of your migration:

```php /** * The database connection that should be used by the migration. * * @var string */ protected $connection = 'pgsql'; /** * Run the migrations. */ public function up(): void { // ... } ``` 

#### Skipping Migrations

Sometimes a migration might be meant to support a feature that is not yet active and you do not want it to run yet. In this case you may define a `shouldRun` method on the migration. If the `shouldRun` method returns `false`, the migration will be skipped:

```php use App\Models\Flights; use Laravel\Pennant\Feature; /** * Determine if this migration should run. */ public function shouldRun(): bool { return Feature::active(Flights::class); } ``` 

## Running Migrations

To run all of your outstanding migrations, execute the `migrate` Artisan command:

```shell php artisan migrate ``` 

If you would like to see which migrations have run thus far, you may use the `migrate:status` Artisan command:

```shell php artisan migrate:status ``` 

If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command:

```shell php artisan migrate --pretend ``` 

#### Isolating Migration Execution

If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command.

When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code:

```shell php artisan migrate --isolated ``` 

To utilize this feature, your application must be using the `memcached`, `redis`, `dynamodb`, `database`, `file`, or `array` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

#### Forcing Migrations to Run in Production

Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag:

```shell php artisan migrate --force ``` 

### Rolling Back Migrations

To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files:

```shell php artisan migrate:rollback ``` 

You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations:

```shell php artisan migrate:rollback --step=5 ``` 

You may roll back a specific "batch" of migrations by providing the `batch` option to the `rollback` command, where the `batch` option corresponds to a batch value within your application's `migrations` database table. For example, the following command will roll back all migrations in batch three:

```shell php artisan migrate:rollback --batch=3 ``` 

If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate:rollback` command:

```shell php artisan migrate:rollback --pretend ``` 

The `migrate:reset` command will roll back all of your application's migrations:

```shell php artisan migrate:reset ``` 

#### Roll Back and Migrate Using a Single Command

The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database:

```shell php artisan migrate:refresh # Refresh the database and run all database seeds... php artisan migrate:refresh --seed ``` 

You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations:

```shell php artisan migrate:refresh --step=5 ``` 

#### Drop All Tables and Migrate

The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command:

```shell php artisan migrate:fresh php artisan migrate:fresh --seed ``` 

By default, the `migrate:fresh` command only drops tables from the default database connection. However, you may use the `--database` option to specify the database connection that should be migrated. The database connection name should correspond to a connection defined in your application's `database` [configuration file](/docs/12.x/configuration):

```shell php artisan migrate:fresh --database=admin ``` 

The `migrate:fresh` command will drop all database tables regardless of their prefix. This command should be used with caution when developing on a database that is shared with other applications.

## Tables

### Creating Tables

To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::create('users', function (Blueprint $table) { $table->id(); $table->string('name'); $table->string('email'); $table->timestamps(); }); ``` 

When creating the table, you may use any of the schema builder's column methods to define the table's columns.

#### Determining Table / Column Existence

You may determine the existence of a table, column, or index using the `hasTable`, `hasColumn`, and `hasIndex` methods:

```php if (Schema::hasTable('users')) { // The "users" table exists... } if (Schema::hasColumn('users', 'email')) { // The "users" table exists and has an "email" column... } if (Schema::hasIndex('users', ['email'], 'unique')) { // The "users" table exists and has a unique index on the "email" column... } ``` 

#### Database Connection and Table Options

If you want to perform a schema operation on a database connection that is not your application's default connection, use the `connection` method:

```php Schema::connection('sqlite')->create('users', function (Blueprint $table) { $table->id(); }); ``` 

In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MariaDB or MySQL:

```php Schema::create('users', function (Blueprint $table) { $table->engine('InnoDB'); // ... }); ``` 

The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MariaDB or MySQL:

```php Schema::create('users', function (Blueprint $table) { $table->charset('utf8mb4'); $table->collation('utf8mb4_unicode_ci'); // ... }); ``` 

The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed:

```php Schema::create('calculations', function (Blueprint $table) { $table->temporary(); // ... }); ``` 

If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MariaDB, MySQL, and PostgreSQL:

```php Schema::create('calculations', function (Blueprint $table) { $table->comment('Business calculations'); // ... }); ``` 

### Updating Tables

The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives a `Blueprint` instance you may use to add columns or indexes to the table:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::table('users', function (Blueprint $table) { $table->integer('votes'); }); ``` 

### Renaming / Dropping Tables

To rename an existing database table, use the `rename` method:

```php use Illuminate\Support\Facades\Schema; Schema::rename($from, $to); ``` 

To drop an existing table, you may use the `drop` or `dropIfExists` methods:

```php Schema::drop('users'); Schema::dropIfExists('users'); ``` 

#### Renaming Tables With Foreign Keys

Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name.

## Columns

### Creating Columns

The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::table('users', function (Blueprint $table) { $table->integer('votes'); }); ``` 

### Available Column Types

The schema builder blueprint offers a variety of methods that correspond to the different types of columns you can add to your database tables. Each of the available methods are listed in the table below:

#### Boolean Types

boolean

#### String & Text Types

char longText mediumText string text tinyText

#### Numeric Types

bigIncrements bigInteger decimal double float id increments integer mediumIncrements mediumInteger smallIncrements smallInteger tinyIncrements tinyInteger unsignedBigInteger unsignedInteger unsignedMediumInteger unsignedSmallInteger unsignedTinyInteger

#### Date & Time Types

dateTime dateTimeTz date time timeTz timestamp timestamps timestampsTz softDeletes softDeletesTz year

#### Binary Types

binary

#### Object & Json Types

json jsonb

#### UUID & ULID Types

ulid ulidMorphs uuid uuidMorphs nullableUlidMorphs nullableUuidMorphs

#### Spatial Types

geography geometry

#### Relationship Types

foreignId foreignIdFor foreignUlid foreignUuid morphs nullableMorphs

#### Specialty Types

enum set macAddress ipAddress rememberToken vector

#### `bigIncrements()`

The `bigIncrements` method creates an auto-incrementing `UNSIGNED BIGINT` (primary key) equivalent column:

```php $table->bigIncrements('id'); ``` 

#### `bigInteger()`

The `bigInteger` method creates a `BIGINT` equivalent column:

```php $table->bigInteger('votes'); ``` 

#### `binary()`

The `binary` method creates a `BLOB` equivalent column:

```php $table->binary('photo'); ``` 

When utilizing MySQL, MariaDB, or SQL Server, you may pass `length` and `fixed` arguments to create `VARBINARY` or `BINARY` equivalent column:

```php $table->binary('data', length: 16); // VARBINARY(16) $table->binary('data', length: 16, fixed: true); // BINARY(16) ``` 

#### `boolean()`

The `boolean` method creates a `BOOLEAN` equivalent column:

```php $table->boolean('confirmed'); ``` 

#### `char()`

The `char` method creates a `CHAR` equivalent column with of a given length:

```php $table->char('name', length: 100); ``` 

#### `dateTimeTz()`

The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional fractional seconds precision:

```php $table->dateTimeTz('created_at', precision: 0); ``` 

#### `dateTime()`

The `dateTime` method creates a `DATETIME` equivalent column with an optional fractional seconds precision:

```php $table->dateTime('created_at', precision: 0); ``` 

#### `date()`

The `date` method creates a `DATE` equivalent column:

```php $table->date('created_at'); ``` 

#### `decimal()`

The `decimal` method creates a `DECIMAL` equivalent column with the given precision (total digits) and scale (decimal digits):

```php $table->decimal('amount', total: 8, places: 2); ``` 

#### `double()`

The `double` method creates a `DOUBLE` equivalent column:

```php $table->double('amount'); ``` 

#### `enum()`

The `enum` method creates a `ENUM` equivalent column with the given valid values:

```php $table->enum('difficulty', ['easy', 'hard']); ``` 

#### `float()`

The `float` method creates a `FLOAT` equivalent column with the given precision:

```php $table->float('amount', precision: 53); ``` 

#### `foreignId()`

The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column:

```php $table->foreignId('user_id'); ``` 

#### `foreignIdFor()`

The `foreignIdFor` method adds a `{column}_id` equivalent column for a given model class. The column type will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type:

```php $table->foreignIdFor(User::class); ``` 

#### `foreignUlid()`

The `foreignUlid` method creates a `ULID` equivalent column:

```php $table->foreignUlid('user_id'); ``` 

#### `foreignUuid()`

The `foreignUuid` method creates a `UUID` equivalent column:

```php $table->foreignUuid('user_id'); ``` 

#### `geography()`

The `geography` method creates a `GEOGRAPHY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier):

```php $table->geography('coordinates', subtype: 'point', srid: 4326); ``` 

Support for spatial types depends on your database driver. Please refer to your database's documentation. If your application is utilizing a PostgreSQL database, you must install the [PostGIS](https://postgis.net) extension before the `geography` method may be used.

#### `geometry()`

The `geometry` method creates a `GEOMETRY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier):

```php $table->geometry('positions', subtype: 'point', srid: 0); ``` 

Support for spatial types depends on your database driver. Please refer to your database's documentation. If your application is utilizing a PostgreSQL database, you must install the [PostGIS](https://postgis.net) extension before the `geometry` method may be used.

#### `id()`

The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column:

```php $table->id(); ``` 

#### `increments()`

The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key:

```php $table->increments('id'); ``` 

#### `integer()`

The `integer` method creates an `INTEGER` equivalent column:

```php $table->integer('votes'); ``` 

#### `ipAddress()`

The `ipAddress` method creates a `VARCHAR` equivalent column:

```php $table->ipAddress('visitor'); ``` 

When using PostgreSQL, an `INET` column will be created.

#### `json()`

The `json` method creates a `JSON` equivalent column:

```php $table->json('options'); ``` 

When using SQLite, a `TEXT` column will be created.

#### `jsonb()`

The `jsonb` method creates a `JSONB` equivalent column:

```php $table->jsonb('options'); ``` 

When using SQLite, a `TEXT` column will be created.

#### `longText()`

The `longText` method creates a `LONGTEXT` equivalent column:

```php $table->longText('description'); ``` 

When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `LONGBLOB` equivalent column:

```php $table->longText('data')->charset('binary'); // LONGBLOB ``` 

#### `macAddress()`

The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column:

```php $table->macAddress('device'); ``` 

#### `mediumIncrements()`

The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key:

```php $table->mediumIncrements('id'); ``` 

#### `mediumInteger()`

The `mediumInteger` method creates a `MEDIUMINT` equivalent column:

```php $table->mediumInteger('votes'); ``` 

#### `mediumText()`

The `mediumText` method creates a `MEDIUMTEXT` equivalent column:

```php $table->mediumText('description'); ``` 

When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `MEDIUMBLOB` equivalent column:

```php $table->mediumText('data')->charset('binary'); // MEDIUMBLOB ``` 

#### `morphs()`

The `morphs` method is a convenience method that adds a `{column}_id` equivalent column and a `{column}_type` `VARCHAR` equivalent column. The column type for the `{column}_id` will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type.

This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/12.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created:

```php $table->morphs('taggable'); ``` 

#### `nullableMorphs()`

The method is similar to the morphs method; however, the columns that are created will be "nullable":

```php $table->nullableMorphs('taggable'); ``` 

#### `nullableUlidMorphs()`

The method is similar to the ulidMorphs method; however, the columns that are created will be "nullable":

```php $table->nullableUlidMorphs('taggable'); ``` 

#### `nullableUuidMorphs()`

The method is similar to the uuidMorphs method; however, the columns that are created will be "nullable":

```php $table->nullableUuidMorphs('taggable'); ``` 

#### `rememberToken()`

The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/12.x/authentication#remembering-users):

```php $table->rememberToken(); ``` 

#### `set()`

The `set` method creates a `SET` equivalent column with the given list of valid values:

```php $table->set('flavors', ['strawberry', 'vanilla']); ``` 

#### `smallIncrements()`

The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key:

```php $table->smallIncrements('id'); ``` 

#### `smallInteger()`

The `smallInteger` method creates a `SMALLINT` equivalent column:

```php $table->smallInteger('votes'); ``` 

#### `softDeletesTz()`

The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality:

```php $table->softDeletesTz('deleted_at', precision: 0); ``` 

#### `softDeletes()`

The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality:

```php $table->softDeletes('deleted_at', precision: 0); ``` 

#### `string()`

The `string` method creates a `VARCHAR` equivalent column of the given length:

```php $table->string('name', length: 100); ``` 

#### `text()`

The `text` method creates a `TEXT` equivalent column:

```php $table->text('description'); ``` 

When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `BLOB` equivalent column:

```php $table->text('data')->charset('binary'); // BLOB ``` 

#### `timeTz()`

The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional fractional seconds precision:

```php $table->timeTz('sunrise', precision: 0); ``` 

#### `time()`

The `time` method creates a `TIME` equivalent column with an optional fractional seconds precision:

```php $table->time('sunrise', precision: 0); ``` 

#### `timestampTz()`

The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision:

```php $table->timestampTz('added_at', precision: 0); ``` 

#### `timestamp()`

The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional fractional seconds precision:

```php $table->timestamp('added_at', precision: 0); ``` 

#### `timestampsTz()`

The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional fractional seconds precision:

```php $table->timestampsTz(precision: 0); ``` 

#### `timestamps()`

The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional fractional seconds precision:

```php $table->timestamps(precision: 0); ``` 

#### `tinyIncrements()`

The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key:

```php $table->tinyIncrements('id'); ``` 

#### `tinyInteger()`

The `tinyInteger` method creates a `TINYINT` equivalent column:

```php $table->tinyInteger('votes'); ``` 

#### `tinyText()`

The `tinyText` method creates a `TINYTEXT` equivalent column:

```php $table->tinyText('notes'); ``` 

When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `TINYBLOB` equivalent column:

```php $table->tinyText('data')->charset('binary'); // TINYBLOB ``` 

#### `unsignedBigInteger()`

The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column:

```php $table->unsignedBigInteger('votes'); ``` 

#### `unsignedInteger()`

The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column:

```php $table->unsignedInteger('votes'); ``` 

#### `unsignedMediumInteger()`

The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column:

```php $table->unsignedMediumInteger('votes'); ``` 

#### `unsignedSmallInteger()`

The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column:

```php $table->unsignedSmallInteger('votes'); ``` 

#### `unsignedTinyInteger()`

The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column:

```php $table->unsignedTinyInteger('votes'); ``` 

#### `ulidMorphs()`

The `ulidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(26)` equivalent column and a `{column}_type` `VARCHAR` equivalent column.

This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/12.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created:

```php $table->ulidMorphs('taggable'); ``` 

#### `uuidMorphs()`

The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column.

This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/12.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created:

```php $table->uuidMorphs('taggable'); ``` 

#### `ulid()`

The `ulid` method creates a `ULID` equivalent column:

```php $table->ulid('id'); ``` 

#### `uuid()`

The `uuid` method creates a `UUID` equivalent column:

```php $table->uuid('id'); ``` 

#### `vector()`

The `vector` method creates a `vector` equivalent column:

```php $table->vector('embedding', dimensions: 100); ``` 

#### `year()`

The `year` method creates a `YEAR` equivalent column:

```php $table->year('birth_year'); ``` 

### Column Modifiers

In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::table('users', function (Blueprint $table) { $table->string('email')->nullable(); }); ``` 

The following table contains all of the available column modifiers. This list does not include index modifiers:

Modifier | Description  
---|---  
`->after('column')` | Place the column "after" another column (MariaDB / MySQL).  
`->autoIncrement()` | Set `INTEGER` columns as auto-incrementing (primary key).  
`->charset('utf8mb4')` | Specify a character set for the column (MariaDB / MySQL).  
`->collation('utf8mb4_unicode_ci')` | Specify a collation for the column.  
`->comment('my comment')` | Add a comment to a column (MariaDB / MySQL / PostgreSQL).  
`->default($value)` | Specify a "default" value for the column.  
`->first()` | Place the column "first" in the table (MariaDB / MySQL).  
`->from($integer)` | Set the starting value of an auto-incrementing field (MariaDB / MySQL / PostgreSQL).  
`->invisible()` | Make the column "invisible" to `SELECT *` queries (MariaDB / MySQL).  
`->nullable($value = true)` | Allow `NULL` values to be inserted into the column.  
`->storedAs($expression)` | Create a stored generated column (MariaDB / MySQL / PostgreSQL / SQLite).  
`->unsigned()` | Set `INTEGER` columns as `UNSIGNED` (MariaDB / MySQL).  
`->useCurrent()` | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` as default value.  
`->useCurrentOnUpdate()` | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` when a record is updated (MariaDB / MySQL).  
`->virtualAs($expression)` | Create a virtual generated column (MariaDB / MySQL / SQLite).  
`->generatedAs($expression)` | Create an identity column with specified sequence options (PostgreSQL).  
`->always()` | Defines the precedence of sequence values over input for an identity column (PostgreSQL).  
  
#### Default Expressions

The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns:

```php <?php use Illuminate\Support\Facades\Schema; use Illuminate\Database\Schema\Blueprint; use Illuminate\Database\Query\Expression; use Illuminate\Database\Migrations\Migration; return new class extends Migration { /** * Run the migrations. */ public function up(): void { Schema::create('flights', function (Blueprint $table) { $table->id(); $table->json('movies')->default(new Expression('(JSON_ARRAY())')); $table->timestamps(); }); } }; ``` 

Support for default expressions depends on your database driver, database version, and the field type. Please refer to your database's documentation.

#### Column Order

When using the MariaDB or MySQL database, the `after` method may be used to add columns after an existing column in the schema:

```php $table->after('password', function (Blueprint $table) { $table->string('address_line1'); $table->string('address_line2'); $table->string('city'); }); ``` 

### Modifying Columns

The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method:

```php Schema::table('users', function (Blueprint $table) { $table->string('name', 50)->change(); }); ``` 

When modifying a column, you must explicitly include all the modifiers you want to keep on the column definition - any missing attribute will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column:

```php Schema::table('users', function (Blueprint $table) { $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change(); }); ``` 

The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column:

```php // Add an index... $table->bigIncrements('id')->primary()->change(); // Drop an index... $table->char('postal_code', 10)->unique(false)->change(); ``` 

### Renaming Columns

To rename a column, you may use the `renameColumn` method provided by the schema builder:

```php Schema::table('users', function (Blueprint $table) { $table->renameColumn('from', 'to'); }); ``` 

### Dropping Columns

To drop a column, you may use the `dropColumn` method on the schema builder:

```php Schema::table('users', function (Blueprint $table) { $table->dropColumn('votes'); }); ``` 

You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method:

```php Schema::table('users', function (Blueprint $table) { $table->dropColumn(['votes', 'avatar', 'location']); }); ``` 

#### Available Command Aliases

Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below:

Command | Description  
---|---  
`$table->dropMorphs('morphable');` | Drop the `morphable_id` and `morphable_type` columns.  
`$table->dropRememberToken();` | Drop the `remember_token` column.  
`$table->dropSoftDeletes();` | Drop the `deleted_at` column.  
`$table->dropSoftDeletesTz();` | Alias of `dropSoftDeletes()` method.  
`$table->dropTimestamps();` | Drop the `created_at` and `updated_at` columns.  
`$table->dropTimestampsTz();` | Alias of `dropTimestamps()` method.  
  
## Indexes

### Creating Indexes

The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::table('users', function (Blueprint $table) { $table->string('email')->unique(); }); ``` 

Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index:

```php $table->unique('email'); ``` 

You may even pass an array of columns to an index method to create a compound (or composite) index:

```php $table->index(['account_id', 'created_at']); ``` 

When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself:

```php $table->unique('email', 'unique_email'); ``` 

#### Available Index Types

Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below:

Command | Description  
---|---  
`$table->primary('id');` | Adds a primary key.  
`$table->primary(['id', 'parent_id']);` | Adds composite keys.  
`$table->unique('email');` | Adds a unique index.  
`$table->index('state');` | Adds an index.  
`$table->fullText('body');` | Adds a full text index (MariaDB / MySQL / PostgreSQL).  
`$table->fullText('body')->language('english');` | Adds a full text index of the specified language (PostgreSQL).  
`$table->spatialIndex('location');` | Adds a spatial index (except SQLite).  
  
### Renaming Indexes

To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument:

```php $table->renameIndex('from', 'to') ``` 

### Dropping Indexes

To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples:

Command | Description  
---|---  
`$table->dropPrimary('users_id_primary');` | Drop a primary key from the "users" table.  
`$table->dropUnique('users_email_unique');` | Drop a unique index from the "users" table.  
`$table->dropIndex('geo_state_index');` | Drop a basic index from the "geo" table.  
`$table->dropFullText('posts_body_fulltext');` | Drop a full text index from the "posts" table.  
`$table->dropSpatialIndex('geo_location_spatialindex');` | Drop a spatial index from the "geo" table (except SQLite).  
  
If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type:

```php Schema::table('geo', function (Blueprint $table) { $table->dropIndex(['state']); // Drops index 'geo_state_index' }); ``` 

### Foreign Key Constraints

Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table:

```php use Illuminate\Database\Schema\Blueprint; use Illuminate\Support\Facades\Schema; Schema::table('posts', function (Blueprint $table) { $table->unsignedBigInteger('user_id'); $table->foreign('user_id')->references('id')->on('users'); }); ``` 

Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so:

```php Schema::table('posts', function (Blueprint $table) { $table->foreignId('user_id')->constrained(); }); ``` 

The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column being referenced. If your table name does not match Laravel's conventions, you may manually provide it to the `constrained` method. In addition, the name that should be assigned to the generated index may be specified as well:

```php Schema::table('posts', function (Blueprint $table) { $table->foreignId('user_id')->constrained( table: 'users', indexName: 'posts_user_id' ); }); ``` 

You may also specify the desired action for the "on delete" and "on update" properties of the constraint:

```php $table->foreignId('user_id') ->constrained() ->onUpdate('cascade') ->onDelete('cascade'); ``` 

An alternative, expressive syntax is also provided for these actions:

Method | Description  
---|---  
`$table->cascadeOnUpdate();` | Updates should cascade.  
`$table->restrictOnUpdate();` | Updates should be restricted.  
`$table->nullOnUpdate();` | Updates should set the foreign key value to null.  
`$table->noActionOnUpdate();` | No action on updates.  
`$table->cascadeOnDelete();` | Deletes should cascade.  
`$table->restrictOnDelete();` | Deletes should be restricted.  
`$table->nullOnDelete();` | Deletes should set the foreign key value to null.  
`$table->noActionOnDelete();` | Prevents deletes if child records exist.  
  
Any additional column modifiers must be called before the `constrained` method:

```php $table->foreignId('user_id') ->nullable() ->constrained(); ``` 

#### Dropping Foreign Keys

To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "_foreign" suffix:

```php $table->dropForeign('posts_user_id_foreign'); ``` 

Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions:

```php $table->dropForeign(['user_id']); ``` 

#### Toggling Foreign Key Constraints

You may enable or disable foreign key constraints within your migrations by using the following methods:

```php Schema::enableForeignKeyConstraints(); Schema::disableForeignKeyConstraints(); Schema::withoutForeignKeyConstraints(function () { // Constraints disabled within this closure... }); ``` 

SQLite disables foreign key constraints by default. When using SQLite, make sure to [enable foreign key support](/docs/12.x/database#configuration) in your database configuration before attempting to create them in your migrations.

## Events

For convenience, each migration operation will dispatch an [event](/docs/12.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class:

Class | Description  
---|---  
`Illuminate\Database\Events\MigrationsStarted` | A batch of migrations is about to be executed.  
`Illuminate\Database\Events\MigrationsEnded` | A batch of migrations has finished executing.  
`Illuminate\Database\Events\MigrationStarted` | A single migration is about to be executed.  
`Illuminate\Database\Events\MigrationEnded` | A single migration has finished executing.  
`Illuminate\Database\Events\NoPendingMigrations` | A migration command found no pending migrations.  
`Illuminate\Database\Events\SchemaDumped` | A database schema dump has completed.  
`Illuminate\Database\Events\SchemaLoaded` | An existing database schema dump has loaded.
