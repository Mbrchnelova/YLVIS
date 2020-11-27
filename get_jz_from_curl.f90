      module read_stuff
      implicit none

      contains
      subroutine read_data_2d(path, x_data, y_data, Bx_data, By_data, &
      Bz_data, noelements)

      implicit none

      integer, intent(inout) :: noelements
      character(len=200), intent(in) :: path
      real, allocatable, intent(inout) :: x_data(:)
      real, allocatable, intent(inout) :: y_data(:)
      real, allocatable, intent(inout) :: Bx_data(:)
      real, allocatable, intent(inout) :: By_data(:)
      real, allocatable, intent(inout) :: Bz_data(:)

      integer :: i, j, k, n, ios
      integer :: read_unit
      
      character(len=100) :: line
      character(len=200), allocatable :: command(:)


      ! First line will be just the number of elements


      read_unit = 102

      open(unit=read_unit, file=trim(path), iostat=ios)

      if ( ios /= 0 ) stop "Error opening file data.dat"

      n = 0

      do
          read(read_unit, '(A)', iostat=ios) line
          if (ios /= 0) exit
          n = n + 1
      end do

      print*, "File contains ", n, "commands"

      allocate(command(n))

      rewind(read_unit)

      do i = 1, n
        read(read_unit, '(A)') command(i)

      end do


      close(read_unit)

      n = 1
      read(command(n), *) noelements


      allocate(x_data(noelements))
      allocate(y_data(noelements))
      allocate(Bx_data(noelements))
      allocate(By_data(noelements))
      allocate(Bz_data(noelements))

      x_data = 0.0
      y_data = 0.0
      Bx_data = 0.0
      By_data = 0.0
      Bz_data = 0.0

      n = 2
      do i = 1, noelements
        read(command(n), *) x_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) y_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) Bx_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) By_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) Bz_data(i)
        n = n + 1
      end do

      end subroutine






      subroutine read_data_3d(path, x_data, y_data, z_data, Bx_data, &
      By_data, Bz_data, noelements)

      implicit none

      integer, intent(inout) :: noelements
      character(len=200), intent(in) :: path
      real, allocatable, intent(inout) :: x_data(:)
      real, allocatable, intent(inout) :: y_data(:)
      real, allocatable, intent(inout) :: z_data(:)
      real, allocatable, intent(inout) :: Bx_data(:)
      real, allocatable, intent(inout) :: By_data(:)
      real, allocatable, intent(inout) :: Bz_data(:)

      integer :: i, j, k, n, ios
      integer :: read_unit

      character(len=100) :: line
      character(len=200), allocatable :: command(:)


      ! First line will be just the number of elements


      read_unit = 102

      open(unit=read_unit, file=trim(path), iostat=ios)

      if ( ios /= 0 ) stop "Error opening file data.dat"

      n = 0

      do
          read(read_unit, '(A)', iostat=ios) line
          if (ios /= 0) exit
          n = n + 1
      end do

      print*, "File contains ", n, "commands"

      allocate(command(n))

      rewind(read_unit)

      do i = 1, n
        read(read_unit, '(A)') command(i)

      end do


      close(read_unit)

      n = 1
      read(command(n), *) noelements


      allocate(x_data(noelements))
      allocate(y_data(noelements))
      allocate(z_data(noelements))
      allocate(Bx_data(noelements))
      allocate(By_data(noelements))
      allocate(Bz_data(noelements))

      x_data = 0.0
      y_data = 0.0
      z_data = 0.0
      Bx_data = 0.0
      By_data = 0.0
      Bz_data = 0.0

      n = 2
      do i = 1, noelements
        read(command(n), *) x_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) y_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) z_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) Bx_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) By_data(i)
        n = n + 1
      end do

      do i = 1, noelements
        read(command(n), *) Bz_data(i)
        n = n + 1
      end do


      end subroutine

      end module











      module curl
      implicit none

      contains
      subroutine compute_2d(noelems, x_data, y_data, Bx_data, By_data, &
      Bz_data, curl_x, curl_y, curl_z, rank, mpisize)

      implicit none

      integer, intent(in) :: noelems, rank, mpisize
      real, dimension(noelems), intent(in) :: x_data
      real, dimension(noelems), intent(in) :: y_data
      real, dimension(noelems), intent(in) :: Bx_data
      real, dimension(noelems), intent(in) :: By_data
      real, dimension(noelems), intent(in) :: Bz_data
      real, dimension(noelems), intent(inout) :: curl_x
      real, dimension(noelems), intent(inout) :: curl_y
      real, dimension(noelems), intent(inout) :: curl_z

      !integer :: ierr
      integer ::  noelems_tocompute, remnant
      !integer :: status(MPI_STATUS_SIZE)

      integer :: ele, f, from, i
      integer :: ind_y_min, ind_y_max, ind_x_min, ind_x_max
      real :: dy, dx, e_x, e_y, f_x, f_y
      real :: dy_min, dy_max, dx_min, dx_max
      real :: Bx, By, Bz
      real :: Bx_in_x, Bx_in_y, Bx_in_z
      real :: By_in_x, By_in_y, By_in_z
      real :: Bz_in_x, Bz_in_y, Bz_in_z
      real :: dy_in_x_min, dy_in_x_max, dx_in_y_min, dx_in_y_max
      real :: curl_Bx, curl_By, curl_Bz
      real :: very_large, very_small


      very_large = 1.0e20
      very_small = 1.0e-20

      !call MPI_INIT(ierr)
      
      !call MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierr) 
      !call MPI_COMM_SIZE(MPI_COMM_WORLD, mpisize, ierr)


      remnant = mod(noelems, mpisize) 

      if (rank < remnant) then
        noelems_tocompute = noelems / mpisize + 1

      else 
        noelems_tocompute = noelems / mpisize

      end if

      do i = 1, noelems_tocompute

        ele = ((i-1) * mpisize) + (rank + 1)

        e_x = x_data(ele)
        e_y = y_data(ele)


        dy_min = very_large
        dy_max = very_large

        dx_min = very_large
        dx_max = very_large

        dy_in_x_min = very_large
        dy_in_x_max = very_large
        dx_in_y_min = very_large
        dx_in_y_max = very_large

        ind_y_min = -1
        ind_x_min = -1
        ind_y_max = -1
        ind_x_max = -1

        do f = 1, noelems
          f_x = x_data(f)
          f_y = y_data(f)

          if (ele /= f) then

            ! The cell to the right
            if (((f_x - e_x) <= dx_max).and.((f_x - e_x) > 0.0)) then
              if (min(dy_in_x_max, abs(f_y-e_y)) == abs(f_y-e_y)) then
                dy_in_x_max = abs(f_y-e_y)
                dx_max = (f_x - e_x)
                ind_x_max = f

              end if
            end if

            ! The cell on the top
            if (((f_y - e_y) <= dy_max).and.((f_y - e_y) > 0.0)) then
              if (min(dx_in_y_max, abs(f_x-e_x)) == abs(f_x-e_x)) then
                dx_in_y_max = abs(f_x-e_x)
                dy_max = (f_y - e_y)
                ind_y_max = f   

              end if
            end if

            ! The cell to the left
            if (((e_x - f_x) <= dx_min).and.((e_x - f_x) > 0.0)) then
              if (min(dy_in_x_min, abs(f_y-e_y)) == abs(f_y-e_y)) then
                dy_in_x_min = abs(f_y-e_y)
                dx_min = (e_x - f_x)
                ind_x_min = f   

              end if
            end if

            ! The cell on the bottom
            if (((e_y - f_y) <= dy_min).and.((e_y - f_y) > 0.0)) then
              if (min(dx_in_y_min, abs(f_x-e_x)) == abs(f_x-e_x)) then
                dx_in_y_min = abs(f_x-e_x)
                dy_min = (e_y - f_y)
                ind_y_min = f   

              end if
            end if

          end if

        end do

        if ((ind_y_min > -1).and.(ind_y_max > -1).and.(ind_x_min > &
     -1).and.(ind_x_max > -1)) then

          dx = x_data(ind_x_max) - x_data(ind_x_min)
          dy = y_data(ind_y_max) - y_data(ind_y_min)

          By_in_y = By_data(ind_y_max) - By_data(ind_y_min)
          Bx_in_y = Bx_data(ind_y_max) - Bx_data(ind_y_min)
          Bz_in_y = Bz_data(ind_y_max) - Bz_data(ind_y_min)

          Bx_in_x = Bx_data(ind_x_max) - Bx_data(ind_x_min)
          Bz_in_x = Bz_data(ind_x_max) - Bz_data(ind_x_min)
          By_in_x = By_data(ind_x_max) - By_data(ind_x_min)

          Bz_in_z = 0.0
          By_in_z = 0.0 
          Bx_in_z = 0.0 


          curl_Bx = Bz_in_y / dy
          curl_By = - Bz_in_x / dx
          curl_Bz = By_in_x / dx - Bx_in_y / dy

          curl_x(ele) = curl_Bx
          curl_y(ele) = curl_By
          curl_z(ele) = curl_Bz


        else

          Bx = Bx_data(ele)
          By = By_data(ele)
          Bz = Bz_data(ele)


          if (ind_x_min > -1) then
            dx = e_x - x_data(ind_x_min)
            Bx_in_x = Bx - Bx_data(ind_x_min)
            By_in_x = By - By_data(ind_x_min)
            Bz_in_x = Bz - Bz_data(ind_x_min)

          else if (ind_x_max > -1) then
            dx = e_x - x_data(ind_x_max)
            Bx_in_x = Bx - Bx_data(ind_x_max)
            By_in_x = By - By_data(ind_x_max)
            Bz_in_x = Bz - Bz_data(ind_x_max)

          else
            print*, "Error determining the nearest cells."
            print*, "Aborting."
            stop 

          end if


          if (ind_y_min > -1) then
            dy = e_y - y_data(ind_y_min)
            Bx_in_y = Bx - Bx_data(ind_y_min)
            By_in_y = By - By_data(ind_y_min)
            Bz_in_y = Bz - Bz_data(ind_y_min)

          else if (ind_y_max > -1) then
            dy = e_y - y_data(ind_y_max)
            Bx_in_y = Bx - Bx_data(ind_y_max)
            By_in_y = By - By_data(ind_y_max)
            Bz_in_y = Bz - Bz_data(ind_y_max)

          else
            print*, "Error determining the nearest cells."
            print*, "Aborting."
            stop

          end if

          Bz_in_z = 0.0
          By_in_z = 0.0 
          Bx_in_z = 0.0 


          curl_Bx = Bz_in_y / dy 
          curl_By = - Bz_in_x / dx
          curl_Bz = By_in_x / dx - Bx_in_y / dy



          curl_x(ele) = 0.0 !curl_Bx
          curl_y(ele) = 0.0 !curl_By
          curl_z(ele) = 0.0 !curl_Bz


        end if




      end do


      end subroutine










      subroutine compute_3d(noelems, x_data, y_data, z_data, Bx_data, &
      By_data, Bz_data, curl_x, curl_y, curl_z, rank, mpisize)

      implicit none

      integer, intent(in) :: noelems, rank, mpisize
      real, dimension(noelems), intent(in) :: x_data
      real, dimension(noelems), intent(in) :: y_data
      real, dimension(noelems), intent(in) :: z_data
      real, dimension(noelems), intent(in) :: Bx_data
      real, dimension(noelems), intent(in) :: By_data
      real, dimension(noelems), intent(in) :: Bz_data
      real, dimension(noelems), intent(inout) :: curl_x
      real, dimension(noelems), intent(inout) :: curl_y
      real, dimension(noelems), intent(inout) :: curl_z

      !integer :: ierr
      integer ::  noelems_tocompute, remnant
      !integer :: status(MPI_STATUS_SIZE)

      integer :: ele, f, from, i
      integer :: ind_y_min, ind_y_max
      integer :: ind_x_min, ind_x_max
      integer :: ind_z_min, ind_z_max
      real :: dy, dx, e_x, e_y, f_x, f_y, dz, e_z, f_z
      real :: dy_min, dy_max, dx_min, dx_max, dz_min, dz_max
      real :: Bx, By, Bz, d
      real :: Bx_in_x, Bx_in_y, Bx_in_z
      real :: By_in_x, By_in_y, By_in_z
      real :: Bz_in_x, Bz_in_y, Bz_in_z
      real :: dyz_in_x_min, dyz_in_x_max
      real :: dxz_in_y_min, dxz_in_y_max
      real :: dxy_in_z_min, dxy_in_z_max
      real :: curl_Bx, curl_By, curl_Bz
      real :: very_large, very_small


      very_large = 1.0e20
      very_small = 1.0e-20

      !call MPI_INIT(ierr)

      !call MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierr) 
      !call MPI_COMM_SIZE(MPI_COMM_WORLD, mpisize, ierr)


      remnant = mod(noelems, mpisize)

      if (rank < remnant) then
        noelems_tocompute = noelems / mpisize + 1

      else
        noelems_tocompute = noelems / mpisize

      end if


      do i = 1, noelems_tocompute

        ele = ((i-1) * mpisize) + (rank + 1)

        e_x = x_data(ele)
        e_y = y_data(ele)
        e_z = z_data(ele)

        dy_min = very_large
        dy_max = very_large

        dx_min = very_large
        dx_max = very_large

        dz_min = very_large
        dz_max = very_large

        dyz_in_x_min = very_large
        dyz_in_x_max = very_large

        dxz_in_y_min = very_large
        dxz_in_y_max = very_large

        dxy_in_z_min = very_large
        dxy_in_z_max = very_large

        ind_y_min = -1
        ind_x_min = -1
        ind_z_min = -1
        ind_y_max = -1
        ind_x_max = -1
        ind_z_max = -1

        do f = 1, noelems
          f_x = x_data(f)
          f_y = y_data(f)
          f_z = z_data(f)


          if (ele /= f) then

            ! The cell to the right
            if (((f_x - e_x) <= dx_max).and.((f_x - e_x) > 0.0)) then
              d = ((f_y-e_y)**2 + (f_z-e_z)**2)**0.5
              if (min(dyz_in_x_max, d) == d) then
                dyz_in_x_max = d
                dx_max = (f_x - e_x)
                ind_x_max = f

              end if
            end if

            ! The cell on the top
            if (((f_y - e_y) <= dy_max).and.((f_y - e_y) > 0.0)) then
              d = ((f_x-e_x)**2 + (f_z-e_z)**2)**0.5
              if (min(dxz_in_y_max, d) == d) then
                dxz_in_y_max = d
                dy_max = (f_y - e_y)
                ind_y_max = f

              end if
            end if

            ! The cell to the left
            if (((e_x - f_x) <= dx_min).and.((e_x - f_x) > 0.0)) then
              d = ((f_y-e_y)**2 + (f_z-e_z)**2)**0.5
              if (min(dyz_in_x_min, d) == d) then 
                dyz_in_x_min = d
                dx_min = (e_x - f_x)
                ind_x_min = f

              end if
            end if

            ! The cell on the bottom
            if (((e_y - f_y) <= dy_min).and.((e_y - f_y) > 0.0)) then
              d = ((f_x-e_x)**2 + (f_z-e_z)**2)**0.5
              if (min(dxz_in_y_min, d) == d) then 
                dxz_in_y_min = d
                dy_min = (e_y - f_y)
                ind_y_min = f

              end if
            end if

            ! The cell in the back 
            if (((e_z - f_z) <= dz_min).and.((e_z - f_z) > 0.0)) then
              d = ((f_x-e_x)**2 + (f_y-e_y)**2)**0.5
              if (min(dxy_in_z_min, d) == d) then
                dxy_in_z_min = d
                dz_min = (e_x - f_x)
                ind_z_min = f

              end if
            end if

            ! The cell in the back 
            if (((f_z - e_z) <= dz_max).and.((f_z - e_z) > 0.0)) then
              d = ((e_x-f_x)**2 + (e_y-f_y)**2)**0.5
              if (min(dxy_in_z_max, d) == d) then
                dxy_in_z_max = d
                dz_max = (f_x - e_x)
                ind_z_max = f

              end if
            end if

          end if

        end do

        if ((ind_y_min > -1).and.(ind_y_max > -1).and.(ind_x_min > &
     -1).and.(ind_x_max > -1).and.(ind_z_min > -1).and.(ind_z_max > &
     -1)) then

          dx = x_data(ind_x_max) - x_data(ind_x_min)
          dy = y_data(ind_y_max) - y_data(ind_y_min)
          dz = z_data(ind_z_max) - z_data(ind_z_min)

          By_in_y = By_data(ind_y_max) - By_data(ind_y_min)
          Bx_in_y = Bx_data(ind_y_max) - Bx_data(ind_y_min)
          Bz_in_y = Bz_data(ind_y_max) - Bz_data(ind_y_min)

          Bx_in_x = Bx_data(ind_x_max) - Bx_data(ind_x_min)
          Bz_in_x = Bz_data(ind_x_max) - Bz_data(ind_x_min)
          By_in_x = By_data(ind_x_max) - By_data(ind_x_min)

          Bz_in_z = Bz_data(ind_z_max) - Bz_data(ind_z_min)
          By_in_z = By_data(ind_z_max) - By_data(ind_z_min)
          Bx_in_z = Bx_data(ind_z_max) - Bx_data(ind_z_min)


          curl_Bx = Bz_in_y / dy - By_in_z / dz
          curl_By = Bx_in_z / dz - Bz_in_x / dx
          curl_Bz = By_in_x / dx - Bx_in_y / dy

          curl_x(ele) = curl_Bx
          curl_y(ele) = curl_By
          curl_z(ele) = curl_Bz


        else

          Bx = Bx_data(ele)
          By = By_data(ele)
          Bz = Bz_data(ele)


          if (ind_x_min > -1) then
            dx = e_x - x_data(ind_x_min)
            Bx_in_x = Bx - Bx_data(ind_x_min)
            By_in_x = By - By_data(ind_x_min)
            Bz_in_x = Bz - Bz_data(ind_x_min)


          else if (ind_x_max > -1) then
            dx = e_x - x_data(ind_x_max)
            Bx_in_x = Bx - Bx_data(ind_x_max)
            By_in_x = By - By_data(ind_x_max)
            Bz_in_x = Bz - Bz_data(ind_x_max)

          else
            print*, "Error determining the nearest cells."
            print*, "Aborting."
            stop

          end if


          if (ind_y_min > -1) then
            dy = e_y - y_data(ind_y_min)
            Bx_in_y = Bx - Bx_data(ind_y_min)
            By_in_y = By - By_data(ind_y_min)
            Bz_in_y = Bz - Bz_data(ind_y_min)

          else if (ind_y_max > -1) then
            dy = e_y - y_data(ind_y_max)
            Bx_in_y = Bx - Bx_data(ind_y_max)
            By_in_y = By - By_data(ind_y_max)
            Bz_in_y = Bz - Bz_data(ind_y_max)

          else
            print*, "Error determining the nearest cells."
            print*, "Aborting."
            stop

          end if

          if (ind_z_min > -1) then
            dz = e_z - z_data(ind_z_min)
            Bx_in_z = Bx - Bx_data(ind_z_min)
            By_in_z = By - By_data(ind_z_min)
            Bz_in_z = Bz - Bz_data(ind_z_min)

          else if (ind_z_max > -1) then
            dz = e_z - z_data(ind_z_max)
            Bx_in_z = Bx - Bx_data(ind_z_max)
            By_in_z = By - By_data(ind_z_max)
            Bz_in_z = Bz - Bz_data(ind_z_max)

          else
            print*, "Error determining the nearest cells."
            print*, "Aborting."
            stop

          end if


          curl_Bx = Bz_in_y / dy - By_in_z / dz
          curl_By = Bx_in_z / dz - Bz_in_x / dx
          curl_Bz = By_in_x / dx - Bx_in_y / dy



          curl_x(ele) = curl_Bx
          curl_y(ele) = curl_By
          curl_z(ele) = curl_Bz


        end if




      end do

      end subroutine
      end module













      program get_curl

      use read_stuff
      use curl

      implicit none

      include 'mpif.h'

      !implicit none

      !use read_stuff
      !use curl


      integer :: rank, ierr, mpisize
      integer :: status(MPI_STATUS_SIZE)

      logical :: is3d
      integer :: i, remnant, from, noelements, ele, noelems_tocompute
      integer :: write_unit, ios
      character(len=200) :: pathin, pathout
      real, allocatable :: x_data(:)
      real, allocatable :: y_data(:)
      real, allocatable :: z_data(:)
      real, allocatable :: Bx_data(:)
      real, allocatable :: By_data(:)
      real, allocatable :: Bz_data(:)
      real, allocatable :: curl_x(:)
      real, allocatable :: curl_y(:)
      real, allocatable :: curl_z(:)
      real, dimension(3) :: curl_all

      character(len=100) :: args
      character(len=2) :: geom

      i = 0

      !path = "data_formatted2.dat"

      do
        call get_command_argument(i, args)
        if (len_trim(args) == 0) EXIT

      !  print*, trim(args)

        i = i+1
        if (i == 2) then
          geom = trim(args)
        else if (i == 3) then
          pathin = trim(args)
        else if (i == 4) then
          pathout = trim(args)
        end if

      end do

     
      call MPI_INIT(ierr)
      call MPI_COMM_RANK(MPI_COMM_WORLD, rank, ierr)
      call MPI_COMM_SIZE(MPI_COMM_WORLD, mpisize, ierr)

      noelements = 0

      if (rank == 0) then
        if (geom == '3d') then
          is3d = .true.
          call read_data_3d(pathin, x_data, y_data, z_data, Bx_data, &
      By_data, Bz_data, noelements)
        else
          is3d = .false.
          call read_data_2d(pathin, x_data, y_data, Bx_data, By_data, &
      Bz_data, noelements)
        end if
      end if


      call MPI_Bcast(noelements, 1, MPI_INT, 0, MPI_COMM_WORLD, ierr) 
      call MPI_Bcast(is3d, 1, MPI_LOGICAL, 0, MPI_COMM_WORLD, ierr) 

      if (rank /= 0) then

        allocate(x_data(noelements))
        allocate(y_data(noelements))
        allocate(Bx_data(noelements))
        allocate(By_data(noelements))
        allocate(Bz_data(noelements))

        if (is3d) then
          allocate(y_data(noelements))
          z_data = 0.0
        end if
       
        x_data = 0.0
        y_data = 0.0
        Bx_data = 0.0
        By_data = 0.0
        Bz_data = 0.0

      end if

      call MPI_Bcast(x_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD, & 
      ierr)
      call MPI_Bcast(y_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD, & 
      ierr)
      call MPI_Bcast(Bx_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD, &
      ierr)
      call MPI_Bcast(By_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD, &
      ierr)
      call MPI_Bcast(Bz_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD, &
      ierr)

      if (is3d) then
        call MPI_Bcast(z_data, noelements, MPI_REAL, 0, MPI_COMM_WORLD,&
      ierr)
      end if


      !print*, "x_data: ", x_data
      !print*, "y_data: ", y_data
      !print*, "Bx_data: ", Bx_data
      !print*, "By_data: ", By_data
      !print*, "Bz_data: ", Bz_data

      print*, "Loaded data. Number of elements: ", noelements

      allocate(curl_x(noelements))
      allocate(curl_y(noelements))
      allocate(curl_z(noelements))
 
      curl_x = 0.0
      curl_y = 0.0
      curl_z = 0.0


      print*, "Initiated MPI of size: ", mpisize

      if (is3d) then
        call compute_3d(noelements, x_data, y_data, z_data, Bx_data, &
      By_data, Bz_data, curl_x, curl_y, curl_z, rank, mpisize)
      else 
        call compute_2d(noelements, x_data, y_data, Bx_data, By_data, &
      Bz_data, curl_x, curl_y, curl_z, rank, mpisize) 
      end if

      print*, rank, "computed curl."

      remnant = mod(noelements, mpisize)
      !print*, "Modulo: ", remnant
      if (rank < remnant) then
        noelems_tocompute = noelements / mpisize + 1

      else
        noelems_tocompute = noelements / mpisize 

      end if

      
      if (rank /= 0) then

        do i = 1, noelems_tocompute

          ele = ((i-1) * mpisize) + (rank + 1)

          !print*, rank, "is sending element:", ele
          curl_all(1) = curl_x(ele)
          curl_all(2) = curl_y(ele)
          curl_all(3) = curl_z(ele)

          call MPI_SEND(curl_all, 3, MPI_REAL, 0, ele, &
      MPI_COMM_WORLD, ierr)

        end do

      end if

      call MPI_Barrier(ierr) 

      print*, rank, "Finished slave work."

      if (rank == 0) then

        do ele = 1, noelements
          from = mod(ele, mpisize) - 1 

          !print*, "Master received ", ele, "from", from
          if (mod(ele, 1000) == 0) print*, "Master received ", ele
          if (from == -1) from = mpisize - 1

          if (from == 0) then
            curl_x(ele) = curl_x(ele)
            curl_y(ele) = curl_y(ele)
            curl_z(ele) = curl_z(ele)

          else 
            call MPI_RECV(curl_all,3, MPI_REAL, from, ele, &
      MPI_COMM_WORLD, status, ierr)   
            
            curl_x(ele) = curl_all(1)
            curl_y(ele) = curl_all(2)
            curl_z(ele) = curl_all(3)

          end if


          if (ele > noelements - 10) print*, "Ele: ", ele, "done."
        end do

      end if

      print*, rank, "Finished data transfer. Writing the final file."

      write_unit = 103
      !pathout = "curl_all.dat"


      if (rank == 0) then
        open(unit=write_unit, file=trim(pathout), iostat=ios)

        do i = 1, noelements
          write(write_unit, *) curl_x(i)
        end do

        do i = 1, noelements
          write(write_unit, *) curl_y(i)
        end do

        do i = 1, noelements
          write(write_unit, *) curl_z(i)
        end do

        close(write_unit) 

      end if

      print*, rank, "Finished master work. Finalizing."

      call MPI_Finalize(ierr)


      end program




