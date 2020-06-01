#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

typedef struct {
  float *arr;
  int size;
} Array;

typedef struct {
  float **arr;
  int size;
  int row;
  int col;
} Array2d;

typedef struct {
  float ***arr;
  int size;
  int i;
  int j;
  int k;
} Array3d;

/*
typedef struct {
  float ****arr;
  int size;
  int i;
  int j;
  int k;
  int h;
} Array4d;
*/

typedef struct {
  float largest_min_regret;
  Array2d *worst_points;
} lower_bound_ret;

//Function Declarations
void arrayInit(Array *a, size_t initialSize);
void arrayAppend(Array *a, float element);
void freeArray(Array *a);
void array2dInit(Array2d *a, int row, int col);
void array2dAppend(Array2d *a, float element);
void free2dArray(Array2d *a);
void array3dInit(Array3d *a, int i, int j, int k);
void array3dAppend(Array3d *a, float element);
void freeArray3d(Array3d *a);
void freelower_bound_ret(lower_bound_ret *lower_bound);
//void lower_upper(int k, int d);
float dot2(Array2d *v1, int x, Array *v2);
float dot3(Array3d *v1, int i, int j, Array *v2);
float regret(Array2d *p, int x, Array3d *points, int i, int utility_repeats);
float set_regret(Array2d *all_points, Array3d *subset, int i, int utility_repeats);
bool find(Array2d *all_points, int x, Array3d *subset, int i, int j);
float smallest_set_regret(Array2d *all_points, int k, int utility_repeats);
void combination(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r);
Array2d* rescaled(Array2d *points);
//void group_search(Array *k_values, Array *d_values, int repeats, int utility_repeats);
//void group_search_compare(Array *k_values, Array *d_values, int repeats, int utility_repeats);
bool dominates(Array2d *set, int x, int y);
bool has_dominances(Array2d *set);
bool compare(Array2d *set, int i, int x);
int choose (int n, int k);
lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats);
//bool one_in_each_dim (Array2d *set);
//lower_bound_ret* grid_search (int k, int d, int n, int c, int utility_repeats);
//lower_bound_ret* refine (int k, int d, int n, float width, int depth, Array2d *points, int utility_repeats);
lower_bound_ret* find_local_maximum (int k, int d, int n, int num_iterations, int utility_repeats);

void arrayInit(Array *a, size_t initialSize)
{
  a->arr = (float *)malloc(initialSize * sizeof(float));
  a->size = 0;
}

void arrayAppend(Array *a, float element)
{
  a->arr[a->size++] = element;
}

void freeArray(Array *a)
{
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
}

void array2dInit(Array2d *a, int row, int col)
{
  a->arr = (float **) malloc(row * sizeof(float *));
  for (int i = 0; i < row; i++)
    a->arr[i] = (float *) malloc(col * sizeof(float));
  a->size = 0;
  a->row = row;
  a->col = col;
}

void array2dAppend(Array2d *a, float element)
{
  a->arr[(int)((a->size)/(a->col))][a->size%a->col] = (float) element;
  a->size++;
}

void free2dArray(Array2d *a)
{
  for (int i = 0; i < a->row; i++)
    free(a->arr[i]);
  free(a->arr);
  a->size = 0;
  a->row = 0;
  a->col = 0;
}

void array3dInit(Array3d *a, int i, int j, int k)
{
  a->arr = (float ***) malloc(i * sizeof(float **));
  for (int l = 0; l < i; l++)
  {
    a->arr[l] = (float **) malloc(j * sizeof(float *));
    for (int m = 0; m < j; m++)
    {
      a->arr[l][m] = (float *) malloc(k * sizeof(float));
    }
  }
  a->size = 0;
  a->i = i;
  a->j = j;
  a->k = k;
}

void array3dAppend(Array3d *a, float element)
{
  a->arr[(int)(a->size)/(a->j * a->k)][(int)(a->size%(a->j * a->k))/(a->k)][(int)(a->size%(a->j * a->k))%(a->k)] = element;
  a->size++;
}

void free3dArray(Array3d *a)
{
  for (int x = 0; x < a->i; x++)
  {
    for (int y = 0; y < a->j; y++)
        free(a->arr[x][y]);
    free(a->arr[x]);
  }
  free(a->arr);
  a->size = 0;
  a->i = 0;
  a->j = 0;
  a->k = 0;
}

void freelower_bound_ret(lower_bound_ret *lower_bound){
  for (int x = 0; x < lower_bound->worst_points->row; x++)
    free(lower_bound->worst_points->arr[x]);
  free(lower_bound->worst_points->arr);
}

/*
void array4dInit(Array4d *a, int i, int j, int k, int h)
{
  a->arr = (float ****) malloc(i * sizeof(float ***));
  for (int l = 0; l < i; l++){
    a->arr[l] = (float ***) malloc(j * sizeof(float **));
    for (int m = 0; m < j; m++){
      a->arr[l][m] = (float **) malloc(k * sizeof(float*));
      for (int n = 0; n < k; n++)
        a->arr[l][m][n] = (float *) malloc(h * sizeof(float));
    }
  }
  a->size = 0;
  a->i = i;
  a->j = j;
  a->k = k;
  a->h = h;
}

void array4dInsert(Array4d *a, Array2d *b, int i, int j)
{
  for (int k = 0; k < b->row; k++)
    for (int h = 0; h < b->col; h++)
      a->arr[i][j][k][h] = b->arr[k][h];
}

void free4dArray(Array4d *a)
{
  for (int x = 0; x < a->i; x++){
    for (int y = 0; y < a->j; y++){
      for (int z = 0; z < a->k; z++)
        free(a->arr[x][y][z]);
      free(a->arr[x][y]);
    }
    free(a->arr[x]);
  }
  free(a->arr);
  a->size = 0;
  a->i = 0;
  a->j = 0;
  a->k = 0;
  a->h = 0;
}

void lower_upper(int k, int d)
{
  float lower = 1 / (8 * pow(2 * k, 2.0/(d-1)));
  float upper = (d - 1.0) / (trunc(pow(k - d + 1, 1.0/(d - 1))) + d - 1);
  printf("%f <= rho(%d,%d) <= %f", lower, k, d, upper);
}
*/

float dot2(Array2d *v1, int i, Array *v2)
{
  float ans = 0;
  for (int j = 0; j < v1->col; j++)
  {
    ans += v1->arr[i][j] * v2->arr[j];
  }
  return ans;
}

float dot3(Array3d *v1, int i, int j, Array *v2)
{
  float ans = 0;
  for (int k = 0; k < v1->k; k++)
  {
    ans += v1->arr[i][j][k] * v2->arr[k];
  }
  return ans;
}

float regret(Array2d *p, int x, Array3d *points, int i, int utility_repeats)
{
  int d = p->col;
  float worst = 0.0;
  //Array *utility = (Array*)malloc(sizeof(Array));
  //arrayInit(utility, d);

  for (int l = 0; l < utility_repeats; l++)
  {
    Array *utility = (Array*)malloc(sizeof(Array));
    arrayInit(utility, d);
    for (int m = 0; m < d; m++)
    {
      float r = (float)rand()/(float)RAND_MAX;
      arrayAppend(utility, r);
    }
    float best = 1.0;
    for (int j = 0; j < points->j; j++)
    {
      float regret = 1.0 - (dot3(points, i, j, utility)/dot2(p, x, utility));
      if (regret < 0)
        regret = 0.0;
      best = fmin(best, regret);
    }
    worst = fmax(worst, best);
    freeArray(utility);
    free(utility);
  }

  //freeArray(utility);
  //free(utility);
  return worst;
}

float set_regret(Array2d *all_points, Array3d *subset, int i, int utility_repeats)
{
  float worst_regret = 0;
  for (int x = 0; x < all_points->row; x++)
  {
    bool ans = false;
    for (int j = 0; j < subset->j; j++)
    {
      ans = ans || find(all_points, x, subset, i, j);
    }
    if (ans == false){
      float point_regret = regret(all_points, x, subset, i, utility_repeats);
      worst_regret = fmax(worst_regret, point_regret);
    }
  }
  return worst_regret;
}

bool find(Array2d *all_points, int x, Array3d *subset, int i, int j){
  bool ans = false;
  for (int y = 0; y < subset->k; y++)
    if (all_points->arr[x][y] == subset->arr[i][j][y])
      ans = true;
    else if (all_points->arr[x][y] != subset->arr[i][j][y])
      return false;
  return ans;
}

float smallest_set_regret(Array2d *all_points, int k, int utility_repeats)
{
  float smallest_regret = 1;
  float worst_regret;

  Array3d *data = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(data, 1, k, all_points->col);

  Array3d *ret = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(ret, choose(all_points->row, k), k, all_points->col);

  combination(all_points, data, ret, 0, all_points->row-1, 0, k);

  for (int i = 0; i < ret->i; i++){
    worst_regret = set_regret(all_points, ret, i, utility_repeats);
    smallest_regret = fmin(smallest_regret, worst_regret);
  }

  free3dArray(data);
  free(data);
  free3dArray(ret);
  free(ret);

  return smallest_regret;
}
  
void combination(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r)
{ 
  if (index == r) 
  { 
    for (int j = 0; j < r; j++)
      for (int k = 0; k < arr->col; k++)
        array3dAppend(ret, data->arr[0][j][k]);
    return; 
  }

  for (int i = start; i <= end && end-i+1 >= r-index; i++) 
  {
    for (int j = 0; j < arr->col; j++)
      data->arr[0][index][j] = arr->arr[i][j];
    combination(arr, data, ret, i+1, end, index+1, r);
  } 
}


Array2d* rescaled(Array2d *points)
{
  int n = points->row;
  int d = points->col;

  Array2d *rescaledpoints = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(rescaledpoints, n, d);

  for (int i = 0; i < d; i++)
  {
    float max = points->arr[0][i];
    for (int j = 1; j < n; j++)
      if (points->arr[j][i] > max)
        max = points->arr[j][i];
    for (int j = 0; j < n; j++)
      rescaledpoints->arr[j][i] = points->arr[j][i]/max;
  }
  return rescaledpoints;
}

/*
void group_search(Array *k_values, Array *d_values, int repeats, int utility_repeats){
  Array2d *bound = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(bound, k_values->size, d_values->size);
  Array2d *count = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(count, k_values->size, d_values->size);

  for (int i = 0; i < k_values->size*d_values->size; i++){
    array2dAppend(bound, 0);
    array2dAppend(count, 0);
  }

  printf("phase 0\n");

  clock_t start_time = clock();
  int iterations = 0;
  int k, d, k_arr, d_arr, min_count;
  while (true){
    k = 0;
    d = 1;
    while (k < d){
      printf("%d\n", rand()%k_values->size);
      k_arr = rand()%k_values->size;
      d_arr = rand()%d_values->size;
      k = k_values->arr[k_arr];
      d = d_values->arr[d_arr];
    }
    count->arr[k_arr][d_arr] += 1;
    iterations++;

    printf("phase 1\n");

    min_count = count->arr[k_arr][d_arr];
    for (int k1 = 0; k1 < k_values->size; k1++)
      for (int d1 = 0; d1 < d_values->size; d1++)
        if (k_values->arr[k1] >= d_values->arr[d1])
          min_count = fmin(count->arr[k1][d1], min_count);

    printf("phase 2\n");

    lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));
    lower_bound = lower_bound_random_search(k, d, k+1, repeats, utility_repeats);
    printf("phase 2\n");
    if (lower_bound->largest_min_regret > bound->arr[k_arr][d_arr])
      bound->arr[k_arr][d_arr] = lower_bound->largest_min_regret;
    
    printf("phase 3\n");

    if (clock() - start_time >= 5.0){ // check if correct
      printf("%d %f", iterations, min_count);

      for (int i = 0; i < d_values->size; i++)
        printf("\t%d ", (int)d_values->arr[i]);
      printf("\n");
      for (int i = 0; i < k_values->size; i++){
        printf("%d ", (int)k_values->arr[i]);
        for (int j = 0; j < d_values->size; j++){
          if (k_values->arr[i] >= d_values->arr[j])
            printf("\t%0.4f ", bound->arr[i][j]);
          else
            printf("\t- ");
        printf("\n");
        }
      printf("\n");
      start_time = clock();
      }
    }
  }
  free2dArray(bound);
  free2dArray(count);
}

void group_search_compare(Array *k_values, Array *d_values, int repeats, int utility_repeats){
  Array2d *bound2 = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(bound2, k_values->size, d_values->size);
  Array2d *bound1 = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(bound1, k_values->size, d_values->size);
  Array2d *count = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(count, d_values->size, d_values->size);

  Array4d *worstpts1 = (Array4d*)malloc(sizeof(Array4d));
  array4dInit(worstpts1, k_values->size, d_values->size, );
  Array4d *worstpts2 = (Array4d*)malloc(sizeof(Array4d));
  array4dInit(worstpts2, k_values->size, d_values->size, );

  for (int k = 0; k < k_values->size*d_values->size; k++){
    array2dAppend(bound2, 0.0);
    array2dAppend(bound1, 0.0);
    array2dAppend(count, 0);
  }

  clock_t start_time = clock();
  int iterations = 0;
  int k, d, k_arr, d_arr, min_count;

  while (true){
    k = 0;
    d = 1;

    while (k < d){
      printf("%d", rand()%k_values->size);
      k_arr = rand()%k_values->size;
      d_arr = rand()%d_values->size;
      k = k_values->arr[k_arr];
      d = d_values->arr[d_arr];
    }
    count->arr[k_arr][d_arr] += 1;
    iterations++;

    min_count = count->arr[k_arr][d_arr];
      for (int k1 = 0; k1 < k_values->size; k1++)
        for (int d1 = 0; d1 < d_values->size; d1++)
          if (k_values->arr[k1] >= d_values->arr[d1])
            min_count = fmin(count->arr[k1][d1], min_count);

    lower_bound_ret *lower_bound = lower_bound_random_search(k, d, k+1, repeats, utility_repeats);
    if (lower_bound->largest_min_regret > bound1->arr[k_arr][d_arr]){
      bound1->arr[k_arr][d_arr] = lower_bound->largest_min_regret;
      lower_bound->worst_points = rescaled(lower_bound->worst_points);
      quickSort(lower_bound->worst_points, 0, lower_bound->worst_points->row-1);
      array4dInsert(worstpts1, lower_bound->worst_points, k_arr, d_arr);
    }

    lower_bound = lower_bound_random_search(k, d, k+2, repeats, utility_repeats);
    if (lower_bound->largest_min_regret > bound2->arr[k_arr][d_arr]){
      bound2->arr[k_arr][d_arr] = lower_bound->largest_min_regret;
      lower_bound->worst_points = rescaled(lower_bound->worst_points);
      quickSort(lower_bound->worst_points, 0, lower_bound->worst_points->row-1);
      array4dInsert(worstpts2, lower_bound->worst_points, k_arr, d_arr);
    }

    if (clock() - start_time >= 5.0){
      printf("%d %f", iterations, min_count);

      printf("With n = k + 1");
      for (int i = 0; i < d_values->size; i++)
        printf("\t%d ", (int)d_values->arr[i]);
      print("\n");
      for (int i = 0; i < k_values->size; i++){
        printf("%d ", (int)k_values->arr[i]);
        for (int j = 0; j < d_values->size; j++){
          if (k_values->arr[i] >= d_values->arr[j]){
            printf("\t%0.4f ", bound1->arr[i][j]); 
            for (int x = 0; x < worstpts1->k; x++)
              for (int y = 0; y < worstpts1->h; y++)
                printf("%f", worstpts1->arr[i][j][x][y]);
          }
          else
            printf("\t- ");
        printf("\n");
        }
      printf("\n");
      }

      printf("With n = k + 2");
      for (int i = 0; i < d_values->size; i++)
        printf("\t%d ", (int)d_values->arr[i]);
      print("\n");
      for (int i = 0; i < k_values->size; i++){
        printf("%d ", (int)k_values->arr[i]);
        for (int j = 0; j < d_values->size; j++){
          if (k_values->arr[i] >= d_values->arr[j]){
            printf("\t%0.4f ", bound2->arr[i][j]); 
            for (int x = 0; x < worstpts2->k; x++)
              for (int y = 0; y < worstpts2->h; y++)
                printf("%f", worstpts2->arr[i][j][x][y]);
          }
          else
            printf("\t- ");
        printf("\n");
        }
      printf("\n");
      }
      start_time = clock();
    }
  }
}
*/

void swap(Array2d * arr, int a, int b){
  for (int i = 0; i < arr->col; i++){
    float temp = arr->arr[a][i];
    arr->arr[a][i] = arr->arr[b][i];
    arr->arr[b][i] = temp;
  }
}

int partition (Array2d *arr, int low, int high){
  float pivot = arr->arr[high][0];
  int i = (low - 1);
  
  for (int j = low; j <= high- 1; j++){
    if (arr->arr[j][0] < pivot){
      i++;
      swap(arr, i, j);
    }
  }
  swap(arr, i + 1, high);
  return (i + 1);
}

void quickSort(Array2d *arr, int low, int high){
  if (low < high){
    int pi = partition(arr, low, high);

    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
  }
}

bool dominates (Array2d *set, int x, int y)
{
  bool strict = false;
  for (int i = 0; i < set->col; i++)
  {
    if (set->arr[x][i] < set->arr[y][i])
    {
      return false;
    }
    else if (set->arr[x][i] > set->arr[y][i])
    {
      strict = true;
    }
  }
  return strict;
}

bool has_dominances(Array2d *set)
{
  for (int i = 0; i < set->row; i++)
  {
    //for (int j = 0; j < set->col; j++)
    {
      for (int x = 0; x < set->row; x++)
      {
        //for (int y = 0; y < set->col; y++)
        if (compare(set, i, x) == true && dominates(set, i, x))
          return true;
      }
    }
  }
  return false;
}

bool compare(Array2d *set, int i, int x){
  bool ans = true;
  for (int j = 0; j < set->col; j++)
  {
    if (set->arr[i][j] != set->arr[x][j])
      return true;
    else if (set->arr[i][j] == set->arr[x][j])
      ans = false;
  }
  return ans;
}

int choose (int n, int k)
{
  int ntok;
  int ktok;

  if (0 <= k && k <= n)
  {
    ntok = 1;
    ktok = 1;
    int min = fmin(k, n-k);
    for (int t = 1; t < min + 1; t++)
    {
      ntok *= n;
      ktok *= t;
      n -= 1;
    }
    return trunc(ntok/ktok);
  }
  else
    return 0;
}

lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats){
  lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));
  lower_bound->largest_min_regret = 0.0;
  lower_bound->worst_points = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(lower_bound->worst_points, n, d);

  for (int r = 0; r < repeats; r++){
    Array2d *points = (Array2d*)malloc(sizeof(Array2d));
    array2dInit(points, n, d);
    for (int i = 0; i < n*d; i++){
      array2dAppend(points, (float)rand()/RAND_MAX);
    }
    
    while (has_dominances(points)){
      free2dArray(points);
      array2dInit(points, n, d);
      for (int i = 0; i < n*d; i++)
        array2dAppend(points, (float)rand()/RAND_MAX);
    }
    
    float smallest_regret = smallest_set_regret(points, k, utility_repeats);
    if (smallest_regret == 1.0)
      smallest_regret = 0.0;
    //printf("%f\n", smallest_regret);

    if (lower_bound->largest_min_regret < smallest_regret){
      lower_bound->largest_min_regret = smallest_regret;
      free2dArray(lower_bound->worst_points);
      array2dInit(lower_bound->worst_points, n, d);
      for (int i = 0; i < n; i++)
        for (int j = 0; j < d; j++)
        {
          //printf("%f \n", points->arr[i][j]);
          lower_bound->worst_points->arr[i][j] = points->arr[i][j];
        }
    }
    free2dArray(points);
    free(points);
  }

  return lower_bound;
}

/*
bool one_in_each_dim (Array2d *set)
{
  int d = set->col;
  Array *largest = (Array*)malloc(sizeof(Array));
  arrayInit(largest, d);

  for (int i = 0; i < d; i++)
    arrayAppend(largest, 0.0);

  for (int point = 0; point < set->size; point++)
    for (int i = 0; i < d; i++)
      largest->arr[i] = fmax(largest->arr[i], set->arr[point][i]);

  for (int i = 0; i < d; i++)
    if (largest->arr[i] < 1.0)
      return false;
  
  freeArray(largest);
  return true;
}


lower_bound_ret* grid_search (int k, int d, int n, int c, int utility_repeats)
{
  Array *chunks = (Array*)malloc(sizeof(Array));
  arrayInit(chunks, c);
  for (int i = 1; i < c+1; i++)
    arrayAppend(chunks, i*(1.0/c));

  lower_bound_ret *ans;
  ans->largest_min_regret = 0;
  ans->worst_points = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(ans->worst_points, n, d);
  int counter = 0;
  int x = pow(c, d);
  int combinations = choose(x, n);

  Array2d *all_cube = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(all_cube, c*c, 2);
  for (int i = 0; i < c; i++)
  {
    for (int j = 0; j < c; j++)
    {
      array2dAppend(all_cube, chunks->arr[i]);
      array2dAppend(all_cube, chunks->arr[j]);
    }
  }
  Array3d *data = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(data, choose(c*c, n), n, d);

  Array3d *ret = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(ret, choose(c*c, n), n, d);

  combination(all_cube, data, ret, 0, all_cube->row-1, 0, n);
  for (int i = 0; i < choose(c*c, n); i++)
  {
    counter += 1;
    if (counter % 1000000 == 0)
      printf("About", 100.0 * counter / combinations, "percent done.");
    if (!has_dominances(ret->arr[i]))
    {
      if (one_in_each_dim(ret->arr[i]))
      {
        float smallest_regret = smallest_set_regret(ret->arr[i], k, utility_repeats);

        if (smallest_regret > ans->largest_min_regret)
        {
          ans->largest_min_regret = smallest_regret;
          ans->worst_points = ret->arr[i];
          printf("", ans->largest_min_regret, ans->worst_points);
        }
      }
    }
  }
  return ans;
}
*/

lower_bound_ret* find_local_maximum (int k, int d, int n, int num_iterations, int utility_repeats){
  lower_bound_ret *lower_bound = lower_bound_random_search(k, d, n, 10, utility_repeats);

  for (int i = 0; i < lower_bound->worst_points->row; i++){
      for (int j = 0; j < lower_bound->worst_points->col; j++)
        printf("%f ", lower_bound->worst_points->arr[i][j]);
      printf("\n");
    }

  Array2d *old_points = (Array2d*)malloc(sizeof(Array2d));
  double epsilon = 0.01;
  int last_change = 0;

  for (int iteration = 0; iteration < num_iterations; iteration++){
    array2dInit(old_points, lower_bound->worst_points->row, lower_bound->worst_points->col);
    for (int i = 0; i < lower_bound->worst_points->row; i++)
      for (int j = 0; j < lower_bound->worst_points->col; j++)
        old_points->arr[i][j] = lower_bound->worst_points->arr[i][j];

    for (int i = 0; i < n; i++)
      for (int j = 0; j < d; j++){
        double max = fmax(0, lower_bound->worst_points->arr[i][j] - epsilon +  2 * epsilon * (float)rand()/RAND_MAX);
        lower_bound->worst_points->arr[i][j] = fmin (1, max);
      }

    lower_bound->worst_points = rescaled(lower_bound->worst_points);
    quickSort(lower_bound->worst_points, 0, lower_bound->worst_points->row-1);
    
    float smallest_regret = smallest_set_regret(lower_bound->worst_points, k, utility_repeats);
    if (smallest_regret == 1.0)
      smallest_regret = 0.0;

    if (lower_bound->largest_min_regret < smallest_regret){
      lower_bound->largest_min_regret = smallest_regret;
      last_change = iteration;
    }

    else {
      for (int i = 0; i < lower_bound->worst_points->row; i++)
        for (int j = 0; j < lower_bound->worst_points->col; j++)
          lower_bound->worst_points->arr[i][j] = old_points->arr[i][j];
    }

    if (iteration - last_change > 1000 && epsilon > 1e-8){
      epsilon = epsilon / 10;
      printf("epsilon = %.17f\n", epsilon);
    }

    if (iteration % 1000 == 0){
      printf("Largest min regret = %f\n", lower_bound->largest_min_regret);
      printf("---Points---\n");
      for (int i = 0; i < lower_bound->worst_points->row; i++){
        for (int j = 0; j < lower_bound->worst_points->col; j++)
          printf("%f ", lower_bound->worst_points->arr[i][j]);
        printf("\n");
      }
    }
    free2dArray(old_points);
  }
  free(old_points);
  return lower_bound;
}

int main ()
{
  //testing find_local_maximum
  clock_t start = clock();

  srand((unsigned)time(NULL));
  
  lower_bound_ret *lower_bound = find_local_maximum(2, 2, 3, 10000, 100);

  freelower_bound_ret(lower_bound);
  free(lower_bound);
  
  //Khoi is Testing vim on linux
  clock_t end = clock();

  float time_taken = (float)(end - start)/CLOCKS_PER_SEC;
  printf("Time taken: %f\n", time_taken);

  /*
  clock_t start = clock();

  srand((unsigned)time(NULL));

  lower_bound_ret *lower_bound = lower_bound_random_search(2, 2, 3, 1000, 1000);
  printf("---Worst Points---\n");
  for (int i = 0; i < lower_bound->worst_points->row; i++){
    for (int j = 0; j < lower_bound->worst_points->col; j++)
      printf("%f ", lower_bound->worst_points->arr[i][j]);
    printf("\n");
  }

  printf("Largest min regret: %f\n", lower_bound->largest_min_regret);
  
  freelower_bound_ret(lower_bound);
  free(lower_bound);

  clock_t end = clock();

  float time_taken = (float)(end - start)/CLOCKS_PER_SEC;
  printf("Time taken: %f\n", time_taken);
  */
  
  
  
  /*
  Array *k_values = (Array*)malloc(sizeof(Array));
  arrayInit(k_values, 5);
  for (int i = 2; i <= 7; i++)
    arrayAppend(k_values, i);

  Array *d_values = (Array*)malloc(sizeof(Array));
  arrayInit(d_values, 5);
  for (int i = 2; i <= 3; i++)
    arrayAppend(d_values, i);

  group_search(k_values, d_values, 1, 100);
  
  freeArray(k_values);
  free(k_values);
  freeArray(d_values);
  free(d_values);
  */

  return 0;
}
