#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

typedef struct {
  float *arr;
  size_t size;
  size_t row;
  size_t col;
} Array;

//Function Declarations
void arrayInit(Array *a, size_t row, size_t col);
void arrayInsert(Array *a, float element);
void freeArray(Array *a);
void lower_upper(int k, int d);
float dot(Array *v1, Array *v2);
float regret(Array *p, Array *points, int utility_repeats);
float set_regret(Array *all_points, Array *subset, int utility_repeats);
//float smallest_set_regret(vector<vector<float>> all_points, int k, int utility_repeats);
Array* rescaled(Array *points);
//bool dominates (vector<float> x, vector<float> y);
//bool has_dominances(vector<vector<float>> set);
//int choose (int n, int k);
//bool one_in_each_dim (vector<vector<float>> set);
//Struct lower_bound_random_search(int k, int d, int n, int = 1000, int = 100);
//void makeCombi(vector<vector<float>> v1, vector<float> v2, int start, int end, int index, int r);

void arrayInit(Array *a, size_t row, size_t col)
{
  int **arr = (float **)malloc(row * sizeof(float *)); 
    for (int i = 0; i < row; i++) 
      arr[i] = (float *)malloc(col * sizeof(float));
  a->size = 0;
  a->row = 0;
  a->col = 0;
}

void arrayInsert(Array *a, float element)
{
  a->size++;
  *(*(a->arr+(a->size % a->row))+(a->size % a->col)) = element;
  a->arr[a->size % a->row][a->size % a->col] = element;
}

void freeArray(Array *a)
{
  for (int i = 0; i < a->row; i++)
    free(a->arr[i]);
  free(a->arr);
  a->size = 0;
  a->row = 0;
  a->col - 0;
}

void lower_upper(int k, int d)
{
  float lower = 1 / (8 * pow(2 * k, 2.0/(d-1)));
  float upper = (d - 1.0) / (trunc(pow(k - d + 1, 1.0/(d - 1))) + d - 1);
  printf("%f <= rho(%d,%d) <= %f", lower, k, d, upper);
}

float dot(Array *v1, Array *v2)
{
  float ans = 0;
  for (int i = 0; i < v1->size; i++)
  {
    ans += v1->arr[i] * v2->arr[i];
  }
  return ans;
}

float regret(Array *p, Array2d *points, int utility_repeats)
{
  if (utility_repeats == NULL)
    utility_repeats = 1000;
  int d = p->size;
  float worst = 0;
  Array *utility;
  arrayInit(utility, d);
  for (int i = 0; i < utility_repeats; i++)
  {
    for (int j = 0; j < d; j++)
    {
      float r = (float) rand()/ (float) RAND_MAX;
      arrayInsert(utility, r);
    }
    float best = 1;
    for (int j = 0; j < points->size; j++)
    {
      float regret = 1 - dot(points->arr[j], utility)/dot(p, &utility);
      best = fmin(best, regret);
    }
    worst = fmax(worst, best);
  }
  return worst;
}

float set_regret(Array2d *all_points, Array2d *subset, int utility_repeats)
{
  if (utility_repeats == NULL)
    utility_repeats = 1000;
  float worst_regret = 0;
  for (int i = 0; i < all_points->size; i++)
  {
    for (int j = 0; i < subset->size; i++)
    {
      if (all_points->arr[i] != subset->arr[j])
      {
        float point_regret = regret(&all_points->arr[i], &subset, utility_repeats);
        worst_regret = fmax(worst_regret, point_regret);
      }
    }
  return worst_regret;
  }
}

float smallest_set_regret(Array2d *all_points, int k, int utility_repeats)
{
  if (utility_repeats == NULL)
    utility_repeats = 1000;
  float smallest_regret = 1;
  //return smallest_set_regret;
}
  
void printCombination(int arr[], int n, int r)
{
  int data[r];
  combinationUtil(arr, data, 0, n-1, 0, r); 
}

void combinationUtil(int arr[], int data[], int start, int end, int index, int r) 
{ 
  if (index == r) 
  {
    for (int j = 0; j < r; j++)
      printf("%d ", data[j]);
    printf("\n");
    return;
  } 
  for (int i =  start; i <= end && end - i + 1 >= r - index; i++) 
  { 
    data[index] = arr[i]; 
    combinationUtil(arr, data, i+1, end, index+1, r);
  }
}

Array2d* rescaled(Array2d *points)
{
  int n = points->size;
  int d = points->col;
  Array2d *rescaledpoints;
  array2dInit(&rescaledpoints, n, d); // check if n is rows and d is cols
  for (int i = 0; i < d; i++)
  {
    float max = points->arr[i];
    for (int j = 1; j < n; j++)
    {
      if (points->arr[j*i] > max)
        max = points->arr[j*i];
    }
    for (int j = 0; j < n; j++)
      rescaledpoints->arr[j*i] = points->arr[j*i]/max;
  }
  return rescaledpoints;
}

bool dominates (Array *x, Array *y)
{
  bool strict = false;
  for (int i = 0; i < x->size; i++)
  {
    if (x->arr[i] < y->arr[i])
    {
      return false;
    }
    else if (x->arr[i] > y->arr[i])
    {
      strict = true;
    }
  }
  return strict;
}

bool has_dominances(Array2d *set)
{
  for (int i = 0; i < set->size; i++)
  {
    for (int j = 0; i < set->size; i++)
    {
      if (set->arr[i] != set->arr[j] && dominates(set->arr[i], set->arr[j]))
      {
        return true;
      }
    }
  }
  return false;
}

int choose (int n, int k)
{
  int ntok = 0;
  int ktok = 0;
  if (0 <= k && k <= n)
  {
    ntok = 1;
    ktok = 1;
    for (int t = 1; t < fmin(k, n-k) + 1; t++)
    {
      ntok *= n;
      ktok *= t;
      n -= 1;
    }
    return trunc(ntok/ktok);
  }
  else
  {
    return 0;
  }
}

bool one_in_each_dim (Array2d *set)
{
  int d = set->col;
  Array *largest;
  arrayInit(largest, d)

  for (int i = 0; i < d; i++)
  {
    largest.push_back(0);
  }
  for (auto point: set)
  {
    for (int i = 0; i < d; i++)
    {
      largest[i] = max(largest[i], point[i]);
    }
  }
  for (int i = 0; i < d; i++)
  {
    if (largest[i] < 1)
    {
      return false;
    }
  }
  return true;
}

Struct lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats)
{
  Struct ans;
  float largest_min_regret = 0;
  vector<vector<float>> worst_points;
  for (int j = 0; j < k+1; j++)
  {
    for (int i = 0; i < d; i++)
    {
      worst_points[j].push_back(0);
    }
  }
  for (int r = 0; r < repeats; r++)
  {
    vector<vector<float>> points;
    for (int j = 0; j < n; j++)
    {
      for (int i = 0; i < d; i++)
      {
        float r = (float) rand()/ (float) RAND_MAX;
        points[j].push_back(r);
      }
    }
    while (has_dominances(points))
    {
      for (int j = 0; j < n; j++)
      {
        for (int i = 0; i < d; i++)
        {
          float r = (float) rand()/ (float) RAND_MAX;
          points[j][i] = r;
        }
      }
    }

float smallest_regret = smallest_set_regret(points, k, utility_repeats);

    if (largest_min_regret < smallest_regret)
    {
      largest_min_regret = smallest_regret;
      worst_points = points;
    }
  }
  ans.largest_min_regret = largest_min_regret;
  ans.worst_points = worst_points;
  return ans;
}

int main ()
{
  srand(time(NULL));

  int arr[] = {1.0, 2.0, 3.0, 4.0, 5.0}; 
  int r = 3; 
  int n = sizeof(arr)/sizeof(arr[0]); 
  printCombination(arr, n, r);
  
  return 0;
}

