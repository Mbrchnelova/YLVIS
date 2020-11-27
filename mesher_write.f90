
      program main

      implicit none

      integer :: i
      character(len=100) :: pathin, pathout
      character(len=100) :: args
      character(len=2) :: geom

      i = 0
      do 
        call get_command_argument(i, args)
        if (len_trim(args) == 0) EXIT

        print*, trim(args)
        i = i+1
        if (i == 2) then
          geom = trim(args)
        else if (i == 3) then
          pathin = trim(args)
        else if (i == 4) then
          pathout = trim(args)
        end if

      end do

      if (i < 1) then
        print*, "Arguments missing. No action taken."

      else if (i < 2) then
        print*, "No input file provided. No action taken."

      else if (i < 3) then
        pathout = "/mesh_converted.neu"
      end if 

      !pathin = "/Users/brch/PhD/Mesher/mesh_upd.neu"
      !pathout = "/Users/brch/PhD/Mesher/mesh_conv.neu"

      if (geom == "2d".or.geom == "2D") then
        call write_2d(pathin, pathout)

      else if (geom == "3d".or.geom == "3D") then
        call write_3d(pathin, pathout)
      else
        print*, "Invalid geometry setting. No action taken."
        print*, "geom:", geom
      end if
 

      end program 




      subroutine write_2d(pathin, pathout)

      integer :: ios 
      integer :: i, n, j, k, write_unit, read_unit, param
      integer :: numnp, nelem, ngrps, nbsets, ndfcd, ndfvl
      integer :: nodidx, cellidx, celltype, nnodes
      integer :: n1, n2, n3, n4
      integer :: c1, c2, c3, c4, c5, c6, c7, c8, c9, c10
      real    :: coordx, coordy

      character(len=100), intent(in) :: pathin, pathout
      character(len=100) :: line 
      character(len=200), allocatable :: command(:)


      write_unit = 101
      read_unit = 102

      !path = "/Users/brch/PhD/Mesher/mesh_upd.neu"
      open(unit=read_unit, file=trim(pathin), iostat=ios)

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

        !print*, command(i)
      end do


      close(read_unit)


      !pathout = "/Users/brch/PhD/Mesher/meshconv.neu"
      open(unit=write_unit, file=trim(pathout), iostat=ios)

      ! Line 1, control info 
      write(write_unit, "(A)") command(1)

      ! Line 2, "** GAMBIT NEUTRAL FILE"
      write(write_unit, "(A)") command(2)


      ! Line 3, user defined title
      write(write_unit, "(A80)") command(3)

      ! Line 4, data source and revision level
      write(write_unit, "('PROGRAM: ',A20, 5X,'VERSION: ', A7)")"brch",&
      "2.6.1"

      ! Line 5, date and time record
      write(write_unit, "(A)") command(5)

      ! Line 6, problem size parameter headingd
      write(write_unit, "(5X,'NUMNP',5X,'NELEM',5X,'NGRPS',4X,'NBSETS',&
      5X,'NDFCD',5X,'NDFVL')")

      ! Line 7, parameters of line 6
      read(command(7), *) numnp
      read(command(8), *) nelem 
      read(command(9), *) ngrps
      read(command(10), *) nbsets
      read(command(11), *) ndfcd
      read(command(12), *) ndfvl


      write(write_unit, "(6(1X,I9))") numnp,nelem,ngrps,nbsets,ndfcd, &
      ndfvl


      ! Line 8, end of section
      write(write_unit, "(A)") command(13)

      ! Line 9, nodal coordinates
      write(write_unit, "(A)") command(14)



      ! Follow up lines - nodal coordinates


      ! Extract nodal coordinates and indices

      j = 15
      do i = 1, numnp

         read(command(j), *) nodidx
         j = j + 1
         read(command(j), *) coordx
         j = j + 1
         read(command(j), *) coordy
         j = j + 1

         write(write_unit, "(I10,2E20.11)") nodidx, coordx, coordy

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! Follow up lines - elements and connectivity
      write(write_unit, "(A)") "      ELEMENTS/CELLS 2.4.6"

      j = j + 2

      do i = 1, nelem

         read(command(j), *) cellidx
         j = j + 1
         read(command(j), *) celltype 
         j = j + 1 
         read(command(j), *) nnodes
         j = j + 1 
         read(command(j), *) n1
         j = j + 1
         read(command(j), *) n2
         j = j + 1
         read(command(j), *) n3
         j = j + 1
         read(command(j), *) n4
         j = j + 1

         write(write_unit, "(I8,1X,I2,1X,I2,1X,7I8)") &    
         !:/(15X,7I8:))") &
         cellidx, celltype, nnodes, n1, n2, n3, n4 

      end do

      write(write_unit, "(A)") "ENDOFSECTION" 

      ! Follow up lines - element groups

      write(write_unit, "(A)") "       ELEMENT GROUP 2.4.6"

      ! Element / group control information

      write(write_unit, "('GROUP: ',I10,' ELEMENTS: ',I10,'MATERIAL: ' &
      I10,' NFLAGS:',I10)") 1, nelem, 2, 1
      write(write_unit, "(A32)") "fluid"
      write(write_unit, "(i8)") 0

      j = j + 7
      i = 0
      do i = 1, nelem/10

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        read(command(j), *) c9
        j = j + 1
        read(command(j), *) c10
        j = j + 1

        write(write_unit, "(10I8)") c1,c2,c3,c4,c5,c6,c7,c8,c9,c10
        !i = i + 10

      end do

      !modnelem = mod(nelem, 10)

      if (mod(nelem, 10) == 1) then
        read(command(j), *) c1
        j = j + 1 
        write(write_unit, "(1I8)") c1


      else if (mod(nelem, 10) == 2) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        write(write_unit, "(2I8)") c1, c2


      else if (mod(nelem, 10) == 3) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(3I8)") c1, c2, c3


      else if (mod(nelem, 10) == 4) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        write(write_unit, "(4I8)") c1, c2, c3, c4


      else if (mod(nelem, 10) == 5) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        write(write_unit, "(5I8)") c1, c2, c3, c4, c5


      else if (mod(nelem, 10) == 6) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        write(write_unit, "(6I8)") c1, c2, c3, c4, c5, c6


      else if (mod(nelem, 10) == 7) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        write(write_unit, "(7I8)") c1, c2, c3, c4, c5, c6, c7


      else if (mod(nelem, 10) == 8) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        write(write_unit, "(8I8)") c1, c2, c3, c4, c5, c6, c7, c8

      else if (mod(nelem, 10) == 9) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        read(command(j), *) c9
        j = j + 1
        write(write_unit, "(9I8)") c1, c2, c3, c4, c5, c6, c7, c8, c9
      
      end if


      j = j + 2 !skipping the endofsection and header
      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n1

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A)") "ENDOFSECTION"

      ! The final lines are the boundary conditions
      write(write_unit, "(A)") "  BOUNDARY CONDITIONS 2.4.6"


      write(write_unit, "(A32, 8I10)") "x0", 1, n1, 0, 6

      do i = 1, n1
       
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! The final lines are the boundary conditions
      write(write_unit, "(A)") "  BOUNDARY CONDITIONS 2.4.6"


      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n2

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "y0", 1, n2, 0, 6

      do i = 1, n2

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! The final lines are the boundary conditions
      write(write_unit, "(A)") "  BOUNDARY CONDITIONS 2.4.6"



      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n3

      j = j + 1 !skipping the number of elements included


      write(write_unit, "(A32, 8I10)") "x1", 1, n3, 0, 6

      do i = 1, n3

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! The final lines are the boundary conditions
      write(write_unit, "(A)") "  BOUNDARY CONDITIONS 2.4.6"


      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n4

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "y1", 1, n4, 0, 6

      do i = 1, n4

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do


      write(write_unit, "(A)") "ENDOFSECTION"



      close(read_unit)
      


      end subroutine











      subroutine write_3d(pathin, pathout)


      integer :: ios
      integer :: i, n, j, k, write_unit, read_unit, param
      integer :: numnp, nelem, ngrps, nbsets, ndfcd, ndfvl
      integer :: nodidx, cellidx, celltype, nnodes
      integer :: n1, n2, n3, n4, n5, n6, n7, n8
      integer :: c1, c2, c3, c4, c5, c6, c7, c8, c9, c10
      real    :: coordx, coordy

      character(len=100), intent(in) :: pathin, pathout
      character(len=100) :: line
      character(len=200), allocatable :: command(:)


      write_unit = 101
      read_unit = 102

      !path = "/Users/brch/PhD/Mesher/mesh_upd.neu"
      open(unit=read_unit, file=trim(pathin), iostat=ios)

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

        !print*, command(i)
      end do


      close(read_unit)


      !pathout = "/Users/brch/PhD/Mesher/meshconv.neu"
      open(unit=write_unit, file=trim(pathout), iostat=ios)

      ! Line 1, control info 
      write(write_unit, "(A)") command(1)

      ! Line 2, "** GAMBIT NEUTRAL FILE"
      write(write_unit, "(A)") command(2)


      ! Line 3, user defined title
      write(write_unit, "(A80)") command(3)

      ! Line 4, data source and revision level
      write(write_unit, "('PROGRAM: ',A20, 5X,'VERSION: ', A7)")"brch",&
      "2.6.1"

      ! Line 5, date and time record
      write(write_unit, "(A)") command(5)

      ! Line 6, problem size parameter headingd
      write(write_unit, "(5X,'NUMNP',5X,'NELEM',5X,'NGRPS',4X,'NBSETS',&
      5X,'NDFCD',5X,'NDFVL')")

      ! Line 7, parameters of line 6
      read(command(7), *) numnp
      read(command(8), *) nelem
      read(command(9), *) ngrps
      read(command(10), *) nbsets
      read(command(11), *) ndfcd
      read(command(12), *) ndfvl


      write(write_unit, "(/6(1X,I9))") numnp,nelem,ngrps,nbsets,ndfcd, &
      ndfvl


      ! Line 8, end of section
      write(write_unit, "(A)") command(13)

      ! Line 9, nodal coordinates
      write(write_unit, "(A)") command(14)



      ! Follow up lines - nodal coordinates


      ! Extract nodal coordinates and indices


      j = 15
      do i = 1, numnp

         read(command(j), *) nodidx
         j = j + 1
         read(command(j), *) coordx
         j = j + 1
         read(command(j), *) coordy
         j = j + 1
         read(command(j), *) coordz
         j = j + 1

         write(write_unit, "(I10,3E20.11)") nodidx,coordx,coordy,coordz

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! Follow up lines - elements and connectivity
      write(write_unit, "(A)") "      ELEMENTS/CELLS 2.4.6"

      j = j + 2

      do i = 1, nelem

         read(command(j), *) cellidx
         j = j + 1
         read(command(j), *) celltype
         j = j + 1
         read(command(j), *) nnodes
         j = j + 1
         read(command(j), *) n1
         j = j + 1
         read(command(j), *) n2
         j = j + 1
         read(command(j), *) n3
         j = j + 1
         read(command(j), *) n4
         j = j + 1
         read(command(j), *) n5
         j = j + 1
         read(command(j), *) n6
         j = j + 1
         read(command(j), *) n7
         j = j + 1
         read(command(j), *) n8
         j = j + 1


         write(write_unit, "(I8,1X,I2,1X,I2,1X,8I8)") &
         !:/(15X,7I8:))") &
         cellidx, celltype, nnodes, n1, n2, n3, n4, n5, n6, n7, n8

      end do

      write(write_unit, "(A)") "ENDOFSECTION"

      ! Follow up lines - element groups

      write(write_unit, "(A)") "       ELEMENT GROUP 2.4.6"

      ! Element / group control information

      write(write_unit, "('GROUP: ',I10,' ELEMENTS: ',I10,'MATERIAL: ' &
      I10,' NFLAGS:',I10)") 1, nelem, 2, 1
      write(write_unit, "(A32)") "fluid"
      write(write_unit, "(i8)") 0


      j = j + 7
      i = 0
      do i = 1, nelem/10

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        read(command(j), *) c9
        j = j + 1
        read(command(j), *) c10
        j = j + 1

        write(write_unit, "(10I8)") c1,c2,c3,c4,c5,c6,c7,c8,c9,c10
        !i = i + 10

      end do

      !modnelem = mod(nelem, 10)

      if (mod(nelem, 10) == 1) then
        read(command(j), *) c1
        j = j + 1
        write(write_unit, "(1I8)") c1


      else if (mod(nelem, 10) == 2) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        write(write_unit, "(2I8)") c1, c2


      else if (mod(nelem, 10) == 3) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(3I8)") c1, c2, c3


      else if (mod(nelem, 10) == 4) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        write(write_unit, "(4I8)") c1, c2, c3, c4


      else if (mod(nelem, 10) == 5) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        write(write_unit, "(5I8)") c1, c2, c3, c4, c5


      else if (mod(nelem, 10) == 6) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        write(write_unit, "(6I8)") c1, c2, c3, c4, c5, c6


      else if (mod(nelem, 10) == 7) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        write(write_unit, "(7I8)") c1, c2, c3, c4, c5, c6, c7


      else if (mod(nelem, 10) == 8) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        write(write_unit, "(8I8)") c1, c2, c3, c4, c5, c6, c7, c8

      else if (mod(nelem, 10) == 9) then
        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        read(command(j), *) c4
        j = j + 1
        read(command(j), *) c5
        j = j + 1
        read(command(j), *) c6
        j = j + 1
        read(command(j), *) c7
        j = j + 1
        read(command(j), *) c8
        j = j + 1
        read(command(j), *) c9
        j = j + 1
        write(write_unit, "(9I8)") c1, c2, c3, c4, c5, c6, c7, c8, c9


      end if


      j = j + 2 !skipping the endofsection and header
      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n1

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A)") "ENDOFSECTION"

      ! The final lines are the boundary conditions
      write(write_unit, "(A)") "  BOUNDARY CONDITIONS 2.4.6"


      write(write_unit, "(A32, 8I10)") "x0", 1, n1, 0, 6

      do i = 1, n1

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do

      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n2

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "y0", 1, n2, 0, 6

      do i = 1, n2

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do



      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n3

      j = j + 1 !skipping the number of elements included


      write(write_unit, "(A32, 8I10)") "x1", 1, n3, 0, 6

      do i = 1, n3

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do


      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n4

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "y1", 1, n4, 0, 6

      do i = 1, n4

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do



      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n5

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "z0", 1, n5, 0, 6

      do i = 1, n5

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do




      j = j + 1 !skipping the x0/x1/y0/y1 headings

      read(command(j), *) n6

      j = j + 1 !skipping the number of elements included

      write(write_unit, "(A32, 8I10)") "z1", 1, n6, 0, 6

      do i = 1, n6

        read(command(j), *) c1
        j = j + 1
        read(command(j), *) c2
        j = j + 1
        read(command(j), *) c3
        j = j + 1
        write(write_unit, "(I10, 2I5)") c1, c2, c3

      end do




      write(write_unit, "(A)") "ENDOFSECTION"



      close(read_unit)



      end subroutine


