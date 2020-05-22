#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

typedef struct {
  float *arr;
  size_t size;
} Array;

typedef struct {
  float *arr;
  size_t size;
} Array2d;

//Function Declarations
void arrayInit(Array *a, size_t initialSize);
void arrayInsert(Array *a, float element);
void freeArray(Array *a);
void array2dInit(Array2d *a, size_t row, size_t col);
void array2dInsert(Array2d *a, float element);
void freeArray2d(Array2d *a);
void lower_upper(int k, int d);
float dot(Array *v1, Array *v2);
float regret(Array *p, Array2d *points, int utility_repeats);
//float set_regret(vector<vector<float>> all_points, vector<vector<float>> subset, int = 1000);
//float smallest_set_regret(vector<vector<float>> all_points, int k, int utility_repeats);
//vector<vector<float>> rescaled(vector<vector<float>> points);
//bool dominates (vector<float> x, vector<float> y);
//bool has_dominances(vector<vector<float>> set);
//int choose (int n, int k);
//bool one_in_each_dim (vector<vector<float>> set);
//Struct lower_bound_random_search(int k, int d, int n, int = 1000, int = 100);
//void makeCombi(vector<vector<float>> v1, vector<float> v2, int start, int end, int index, int r);

//https://stackoverflow.com/questions/3536153/c-dynamically-growing-array

void arrayInit(Array *a, size_t initialSize)
{
  a->arr = (float *)malloc(initialSize * sizeof(float));
  a->size = 0;
}

void arrayInsert(Array *a, float element)
{
  a->arr[a->size++] = element;
}

void freeArray(Array *a)
{
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
}

//https://www.tutorialspoint.com/how-to-dynamically-allocate-a-2d-array-in-c

void array2dInit(Array2d *a, size_t row, size_t col)
{
  a->arr = (float *)malloc(row * col * sizeof(float));
  a->size = 0;
}

void array2dInsert(Array2d *a, float element)
{
  a->arr[a->size++] = element;
}

void freeArray2d(Array2d *a)
{
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
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
  int d = sizeof(p);
  float worst = 0;
  Array utility;
  arrayInit(&utility, d);
  for (int i = 0; i < utility_repeats; i++)
  {
    for (int j = 0; j < d; j++)
    {
      float r = (float) rand()/ (float) RAND_MAX;
      arrayInsert(&utility, r);
    }
    float best = 1;
    for (int j = 0; j < sizeof(points); j++)
    {
      float regret = 1 - dot(&points->arr[j], &utility)/dot(p, &utility);
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
  for (int i = 0; i < sizeof(all_points); i++)
  {
    for (int j = 0; i < sizeof(subset); i++)
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

int main ()
{
  srand(time(NULL));

  int arr[] = {1.0, 2.0, 3.0, 4.0, 5.0}; 
  int r = 3; 
  int n = sizeof(arr)/sizeof(arr[0]); 
  printCombination(arr, n, r);
  
  return 0;
}

